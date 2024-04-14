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

        return [news_id, self.id, vote, self.trust]
    
    def get_trust(self):
        # return trust of voter
        return self.trust

    def inc_trust(self):
        # increase trust of voter
        self.trust_history.append(self.trust)
        self.trust += np.exp(-self.trust/100)
        # trust is always between 0 and 100
        if self.trust > 100:
            self.trust = 100
        
    def dec_trust(self):
        # decrease trust of voter
        self.trust_history.append(self.trust)
        self.trust -= np.exp(-self.trust/100)
        # trust is always between 0 and 100
        if self.trust < 0:
            self.trust = 0

class news():
    def __init__(self, id):
        self.id = id
        self.votes = []

    def election(self, voters):
        for peer in voters:
            vote = peer.vote(self.id)
            self.votes.append(vote)

    def get_rating(self):
        # return rating of news
        # rating is number of votes for news
        rating = float(0);
        totat_trust = float(0);
        for vote in self.votes:
            rating += vote[2]*vote[3]
            totat_trust += vote[3]
        
        return rating/totat_trust > 0.5

    def fact_check(self, voters, result):
        # increase trust of voters who voted news correctly
        # decrease trust of voters who voted news incorrectly
        for i, peer_vote in enumerate(self.votes):
            peer = voters[i]
            if peer_vote[2] == result:
                peer.inc_trust()
            else:
                peer.dec_trust()

# create N voters, N must be Integer
N = int(input("Enter number of voters: "))

# q is fraction of malicious voters
q = float(input("Enter fraction of malicious voters(q): "))

# p is fraction of voters having more probability of voting correctly among 1-q
p = float(input("Enter fraction of voters having more probability of voting correctly(p): "))

# finally N*q are 0, N*(1-q)*p are 1, and N*(1-q)*(1-p) are 2
voters = []
mallecious = int(N * q)
honest = int(N * (1 - q) * p)
for i in range(N):
    # create voters
    if i < mallecious:
        voters.append(voter(i, 0))
    elif i < mallecious + honest:
        voters.append(voter(i, 1))
    else:
        voters.append(voter(i, 2))

# shuffle voters
np.random.shuffle(voters)

# create M news, M must be Integer
M = int(input("Enter number of news: "))

for i in range(M):
    # all news are true
    current_news = news(i)
    # conduct election
    current_news.election(voters)
    # get rating of news
    rating = current_news.get_rating()
    print("Rating of news", i, "is", rating)
    # fact check
    current_news.fact_check(voters, rating)
# calculate average trust of voters
avaerage_history_honest = [0 for i in range(M)]
avaerage_history_mallicious = [0 for i in range(M)]
avaerage_history_semi_honest = [0 for i in range(M)]
for i in range(N):
    if voters[i].is_honest == 0:
        for j in range(M):
            avaerage_history_mallicious[j] += voters[i].trust_history[j]
    elif voters[i].is_honest == 1:
        for j in range(M):
            avaerage_history_honest[j] += voters[i].trust_history[j]
    else:
        for j in range(M):
            avaerage_history_semi_honest[j] += voters[i].trust_history[j]

avaerage_history_honest = [x /honest for x in avaerage_history_honest]
avaerage_history_semi_honest = [x / (N - honest - mallecious) for x in avaerage_history_semi_honest]
avaerage_history_mallicious = [x / (mallecious) for x in avaerage_history_mallicious]

# plot average trust of voters
plt.plot(avaerage_history_honest, label='Honest')
plt.plot(avaerage_history_semi_honest, label='Semi-Honest')
plt.plot(avaerage_history_mallicious, label='Malicious')
plt.xlabel('News')
plt.ylabel('Average Trust')
plt.legend()
plt.savefig('trust.png')
plt.show()