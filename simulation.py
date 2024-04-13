import numpy as np
import matplotlib.pyplot as plt

class voter():
    def __init__(self, id, is_honest):
        self.id = id
        # trust is a number between 0 and 100
        # initially set to 50
        self.trust = 50
        self.is_honest = is_honest
        self.trust_history = []
    
    def vote(self, news_id):
        # if is_honest=2 vote 1 with probability 0.7 and 0 with probability 0.3
        # if is_honest=1 vote 1 with probability 0.9 and 0 with probability 0.1
        # if is_honest=0 vote 0 with probability 1
        vote = 0
        if self.is_honest == 2:
            vote = np.random.choice([0, 1], p=[0.3, 0.7])
        elif self.is_honest == 1:
            vote = np.random.choice([0, 1], p=[0.1, 0.9])

        return [news_id, self.id, vote]
    
    def get_trust(self):
        return self.trust

    def inc_trust(self):
        self.trust_history.append(self.trust)
        self.trust += np.exp(-self.trust/100)
        if self.trust > 100:
            self.trust = 100
        
    def dec_trust(self):
        self.trust_history.append(self.trust)
        self.trust -= np.exp(-self.trust/100)
        if self.trust < 0:
            self.trust = 0

class news():
    def __init__(self, id, is_fake):
        self.id = id
        self.is_fake = is_fake
        self.votes = []

    def election(self, voters):
        for peer in voters:
            vote = peer.vote(self.id)
            self.votes.append(vote)

    def fact_check(self, voters):
        # increase trust of voters who voted news correctly
        # decrease trust of voters who voted news incorrectly
        for i, peer_vote in enumerate(self.votes):
            peer = voters[i]
            if peer_vote[2] == self.is_fake:
                peer.inc_trust()
            else:
                peer.dec_trust()

# create N voters, N must be Integer
N = int(input("Enter number of voters: "))

# q is fraction of malicious voters
q = float(input("Enter fraction of malicious voters: "))

# p is fraction of voters having more probability of voting correctly among 1-q
p = float(input("Enter fraction of voters having more probability of voting correctly: "))

# finally N*q are 0, N*(1-q)*p are 1, and N*(1-q)*(1-p) are 2
voters = []
for i in range(N):
    if i < N * q:
        voters.append(voter(i, 0))
    elif i < N * (1 - q) * p:
        voters.append(voter(i, 1))
    else:
        voters.append(voter(i, 2))

# shuffle voters
np.random.shuffle(voters)

# create M news, M must be Integer
M = int(input("Enter number of news: "))

for i in range(M):
    # all news are true
    current_news = news(i, 1)
    # conduct election
    current_news.election(voters)
    # fact check
    current_news.fact_check(voters)

avaerage_history = [0 for i in range(M)]
for i in range(N):
    for j in range(M):
        avaerage_history[j] += voters[i].trust_history[j]

avaerage_history = [x / N for x in avaerage_history]
    


# plot trust history of voters for each votes create trust_history_id.png where x is range(0, M) and Y is trust_history of voter
for i in range(N):
    s = "mallicious" if voters[i].is_honest == 0 else "honest" if voters[i].is_honest == 1 else "semi-honest"
    plt.xlabel('news_id')
    plt.ylabel('Trust')
    plt.title('Trust History of Voter ' + str(i)+" " + s)
    # make a gunplot of dots for trust_history
    plt.plot(range(0, M), voters[i].trust_history, 'ro')
    # make a gunplot of dots for average_history
    plt.plot(range(0, M), avaerage_history, 'bo')
    plt.legend(['Voter Trust', 'Average Trust'])
    plt.savefig('trust_history_' + str(i) + '.png')
    plt.clf()
