# Chemical Stack
## Game Mechanics
Chemical Stack is a 2-player game lasting 8 rounds (with a possible tiebreaker round) that uses the periodic table to let chemists compete by creating stacks of elements.
### Basic Rules
1. Each player gets a deck of 55 random elements and a **stack** is created of the remaining 8 elements.
2. Each element in the **stack** represents a round where each player has the opportunity to _"stack"_ as many of their elements as possible.
3. Players can _stack_ their elements in one of two ways each round:
  - Matching starting letters of elements (ex. **Stack Element:** Carbon and _Player 1 Element:_ Caclium).
  - Elements within + or - 10 atomic mass units of each either (ex. **Stack Element:** Carbon and _Player 1 Element:_ Oxygen).
4. Whichever player can _stack_ more of the elements from their deck to the round's **stack** element, wins the round.
  - Players are allowed to _stack_ both ways each round (ex. Player 1 would get a point for both Calcium and Oxygen).
  - If the two players tie for the round, neither gets a point.
5. At the end of 8 rounds, whoever has more points is the winner!
  - However, it is possible there is a tie after 8 rounds and that's where the real fun begins!

### Tiebreaker Round
1. Define tiebreaker here!!!

## Code Execution
Chemical Stack is defined in the Game class and can be run as many times as desired in the main method.
1. Start by creating an instantiation of the Game class with the names of the two players.
2. Upon instantiation, the game immediately generates players decks and the stack for the game. The method "decks_and_stack" prints each players deck and the stack
3. The play method can then be called to simulate the game
  - Within the play method, play_round and play_tiebreaker are called to help simulate the game
  - Each round, the number and winner of the round is printed
4. At the end of the game, the winner will be printed
5. Additional stats from the game can be printed using the stats method

<img width="857" height="97" alt="image" src="https://github.com/user-attachments/assets/22c5d786-0e6a-4cc2-999c-4ca19fe60d74" />

6. To play more rounds, use the reset method to redraw the decks and stack
7. After that, use the same methods from above to play more rounds!

<img width="782" height="87" alt="image" src="https://github.com/user-attachments/assets/89d3d403-c74b-4522-a7db-a0e955d983d5" />

8. Lastly, a new game can be created with two new chemists as shown below.
9. Once the new game is created follow all previous steps the play!

<img width="931" height="105" alt="image" src="https://github.com/user-attachments/assets/715939d2-96d4-42f5-85b1-e958f8471a1e" />


