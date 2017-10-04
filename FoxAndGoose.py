import sys

class Node:
    color = 0; # '0' means white, '1' means black;
    index = 0; # The number of each node;
    link = []; # Contains nodes connected to the current node -> list

    def __init__(self,index,color,link):
        self.index = index;
        self.color = color;
        self.link = link;

# Initial Positions
# Each position has a corresponding number
pos_hound1 = 0; # Number 0
pos_hound2 = 1; # Number 1
pos_hound3 = 3; # Number 2
pos_hare = 10;  # Number 3

ListForPos = [];

ListForPos.append(Node(0,0,[1,2,3]));
ListForPos.append(Node(1,0,[0,2,4,5]));
ListForPos.append(Node(2,0,[0, 1, 3, 5]));
ListForPos.append(Node(3,0,[0, 2 ,6]));
ListForPos.append(Node(4,0,[1,5,7]));
ListForPos.append(Node(5,0,[1, 2, 3, 4, 6, 7, 8, 9]));
ListForPos.append(Node(6,0,[3,6,5]));
ListForPos.append(Node(7,0,[4,5,8,10]));
ListForPos.append(Node(8,0,[5,7,9,10]));
ListForPos.append(Node(9,0,[5,6,8]));
ListForPos.append(Node(10,0,[7,8,9]));

ListForPos[pos_hound1].color = 1;
ListForPos[pos_hound2].color = 1;
ListForPos[pos_hound3].color = 1;
ListForPos[pos_hare].color = 1;

# function: GenerateMove
# parameter: index = []
# return value: move = []
# index is a list contains all moving objects each turn.
# For instance: hounds' turn -> index=[pos_hound1,pos_hound2,pos_hound3];
#               hare's turn  -> index=[pos_hare];
def GenerateMove(index):
    move = [];
    for EachObject in index:
        for EachConnection in ListForPos[EachObject].link:
            if ListForPos[EachConnection].color < 1:
                if ListForPos[EachConnection].index not in move:
                    move.append(ListForPos[EachConnection].index);
    return move;

# function: primitive
# parameter: move = []
# return value: 0/1
# move is a list contains all reachable spots.
# if there's nothing in move, then the guy loses.
def primitive(move):
    HoundsWin = 1;
    if(pos_hare == 0):
        return "Hare win!";
    for i in ListForPos[pos_hare].link:
        if(ListForPos[i].color == 0):
            HoundsWin = 0;
            break;
    if(HoundsWin):
        return "Hounds win!";
    else:
        return "Game continues..."

def DoMove(ObjNumber, InitPos, TargetPos):
    global pos_hound1, pos_hound2, pos_hound3, pos_hare;
    if ObjNumber not in [0,1,2,3]:
        print("Input a wrong Object Number!");
    elif TargetPos not in GenerateMove([InitPos]):
        print("Input a wrong movement!");
    else:
        if(ObjNumber == 0):
            if(pos_hound1 == InitPos):
                pos_hound1 = TargetPos;
                ListForPos[InitPos].color = 0;
                ListForPos[TargetPos].color = 1;
            else:
                print("Initial position doesn't match with the object number!");
        elif(ObjNumber == 1):
            if(pos_hound2 == InitPos):
                pos_hound2 = TargetPos;
                ListForPos[InitPos].color = 0;
                ListForPos[TargetPos].color = 1;
        elif(ObjNumber == 2):
            if(pos_hound3 == InitPos):
                pos_hound3 = TargetPos;
                ListForPos[InitPos].color = 0;
                ListForPos[TargetPos].color = 1;
        else:
            if(pos_hare == InitPos):
                pos_hare = TargetPos;
                ListForPos[InitPos].color = 0;
                ListForPos[TargetPos].color = 1;

# Test

#PossibleMove = GenerateMove([pos_hound2]);
#print(PossibleMove);

#print(primitive(GenerateMove([pos_hare])));

DoMove(1,pos_hound2,2);
print(pos_hound2, ListForPos[1].color, ListForPos[2].color);
