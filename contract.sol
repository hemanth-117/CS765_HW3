// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity >=0.8.0 <0.9.0;

contract Dap {
    struct Voter {
        // id of voter
        uint id;
        // name of voter
        string name;
        // trust score of voter
        uint trustScore;
        // money to be deposited by voter for voting 
        uint money;
        // is voter valid
        bool isVoter;
    }

    struct Vote {
        // id of voter
        uint voterId;
        // id of news which he voted
        uint newsId;
        // rating of news by voter
        uint rating;
    }
    
    struct News {
        // id of news
        uint id;
        // news content
        string news;
        // list of votes on news
        Vote[] votes;
        // total votes on news
        uint totalVotes;
        // is news valid
        bool isNews;
        // category of news
        uint category;
        // voter who added the news
        uint voterId;
    }
    // list of voters
    mapping(uint => Voter) public voters;
    // list of news
    mapping(uint => News) public newsList;
    // total number of voters
    uint public voterCount;
    // total number of news
    uint public newsCount;

    function addVoter(string memory _name, uint _money) public {
        // check if voter is already added
        for(uint i = 1; i <= voterCount; i++) {
            require(keccak256(abi.encodePacked(voters[i].name)) != keccak256(abi.encodePacked(_name)), "Voter already exists");
        }
        voterCount++;
        voters[voterCount] = Voter(voterCount, _name, 50 , _money,true);
    }

    function addNews(string memory _news, uint _category, uint _vid) public {
        // check if voter is valid
        require(voters[_vid].isVoter == true, "Invalid voter");
        // check if he has enough money to add news
        require(voters[_vid].money >= 50, "Not enough money");
        // check if news is already added
        for(uint i = 1; i <= newsCount; i++) {
            require(keccak256(abi.encodePacked(newsList[i].news)) != keccak256(abi.encodePacked(_news)), "News already exists");
        }
        newsCount++;
        newsList[newsCount] = News(newsCount, _news, new Vote[](0), 0, true, _category, _vid);
        // deposit 50 money as proof of adding news
        voters[_vid].money -= 50;
    }

    function voteNews(uint _voterId, uint _newsId, uint _rating) public {
        // check if voter is valid and news is valid and rating is valid
        require(voters[_voterId].isVoter == true, "Invalid voter");
        require(newsList[_newsId].isNews == true, "Invalid news");
        require(_rating == 0 || _rating == 1, "Rating should be between 0 or 1");
        // check if voter has 100 money
        require(voters[_voterId].money >= 10, "Not enough money");
        // deposit 100 money as proof of voting
        voters[_voterId].money -= 10;
        // add vote to news
        newsList[_newsId].votes.push(Vote(_voterId, _newsId, _rating));
        // increment total votes of news
        newsList[_newsId].totalVotes++;
    }

    function getNewsRating(uint _newsId) public view returns(uint) {
        // check if news is valid
        require(newsList[_newsId].isNews == true, "Invalid news");
        // total rating of a news item is sum(trustScore of voter * rating of voter)/sum(trustScore of voter)
        uint totalRating = 0;
        for(uint i = 0; i < newsList[_newsId].votes.length; i++) {
            // find contribution of each voter to the total rating
            totalRating += voters[newsList[_newsId].votes[i].voterId].trustScore * newsList[_newsId].votes[i].rating;
        }
        return totalRating;
    }

    function factcheck(uint _newsId, uint _is_true) public {
        // check if news is valid
        require(newsList[_newsId].isNews == true, "Invalid news");
        // check if _is_true is valid
        require(_is_true == 0 || _is_true == 1, "Invalid input");
        uint confiscate = 0;
        // if news is valid, give the deposit back to the voter who added the news
        if(_is_true == 1) {
            voters[newsList[_newsId].voterId].money += 50;
        }
        else {
            // if news is invalid, confiscate the deposit of the voter who added the news
            confiscate += 50;
        }
        // assuming he votes correctly for his own news
        uint voted_correctly = 0;
        for(uint i = 0; i < newsList[_newsId].votes.length; i++) {
            // update trust score of voters based on their vote
            // add 1 if voter voted correctly, else subtract 1
            if(_is_true == newsList[_newsId].votes[i].rating) {
                // increment trust score of voter if he voted correctly
                voters[newsList[_newsId].votes[i].voterId].trustScore += 1;
                // give their deposit to voter if he voted correctly
                voters[newsList[_newsId].votes[i].voterId].money += 10; 
                // increment number of voters who voted correctly
                voted_correctly++;  
            }
            else {
                // decrement trust score of voter if he voted incorrectly
                voters[newsList[_newsId].votes[i].voterId].trustScore -= 1;
                // confiscate their deposit if he voted incorrectly
                confiscate += 10;

            }
            // check if trust score is between 0 and 100
            if(voters[newsList[_newsId].votes[i].voterId].trustScore > 100) {
                voters[newsList[_newsId].votes[i].voterId].trustScore = 100;
            }
            if(voters[newsList[_newsId].votes[i].voterId].trustScore < 0) {
                voters[newsList[_newsId].votes[i].voterId].trustScore = 0;
            }
        }
        // confiscate money of voters who voted incorrectly
        // give the money to them who voted correctly equally
        uint reward = confiscate/voted_correctly;
        for(uint i = 0; i < newsList[_newsId].votes.length; i++) {
            if(_is_true == newsList[_newsId].votes[i].rating) {
                // incentivize voters who voted correctly
                voters[newsList[_newsId].votes[i].voterId].money += reward;
            }
        }
    }
}