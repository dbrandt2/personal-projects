import random

class Node:
	def __init__(self, key):
		self.key = key;
		self.right = None;
		self.left = None;
		self.height = 1; 

def RotateRight(y):
	x = y.left;
	T2 = x.right;
	x.right = y;
	y.left = T2;
	y.height = Max(Height(y.left), Height(y.right)) + 1;
	x.height = Max(Height(x.left), Height(x.right)) + 1;
	return x;

def RotateLeft(x):
	y = x.right;
	T2 = y.left;
	y.left = x;
	x.right = T2;
	x.height = Max(Height(x.left), Height(x.right)) + 1;
	y.height = Max(Height(y.left), Height(y.right)) + 1;
	return y;

#return the max number
def Max(a, b):
	if (a > b):
		return a;
	else:
		return b;

def Balance(curr):
	if curr == None:
		return 0;
	return (Height(curr.left) - Height(curr.right));

def Height(curr):
	if curr == None:
		return 0;
	return curr.height

def MakeRoot(key):
	return Node(key);

def Insert(curr, key):
	if (curr == None):
		return Node(key);
	if (key < curr.key):
		curr.left = Insert(curr.left, key);
	else:
		curr.right = Insert(curr.right, key);
	curr.height = max(Height(curr.left), Height(curr.right)) + 1;
	balance = Balance(curr);
	#print(balance);

	#these next line will determine and rebalance tree if needed
	#Left left inbalance
	if (balance > 1 and key < curr.left.key):
		return RotateRight(curr);

	#Right right inbalance
	if (balance < -1 and key > curr.right.key):
		return RotateLeft(curr);

	#Left right inbalance
	if (balance > 1 and key > curr.left.key):
		curr.left = RotateLeft(curr.left);
		return RotateRight(curr);

	#Right left inbalance
	if(balance < -1 and key < curr.right.key):
		curr.right = RotateRight(curr.right);
		return RotateLeft(curr);

	return curr;

def PreOrder(x):

	if (x == None):
		return;
	
	print(x.key);

	PreOrder(x.left);
	
	PreOrder(x.right);
	return 0;

def PrintTree(x, level = 0):
	if x != None:
		PrintTree(x.left, level + 1)
		print(' ' * 4 * level + '->', x.key)
		PrintTree(x.right, level + 1)

def main():
	root = MakeRoot(10);
	for x in range(0, 5):
		root = Insert(root, random.randint(0, 100));
	#print(root.key);
	PrintTree(root)
	#PreOrder(root);


if __name__ == "__main__":
	main()
