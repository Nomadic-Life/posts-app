from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to find a pair in an array with a given sum using hashing
def findPair(nums, target):
 
    # create an empty dictionary
    d = {}
    pair_found = False 

    # do for each element
    for i, e in enumerate(nums):
 
        # check if pair (e, target - e) exists
        # if the difference is seen before, print the pair
        if target - e in d:
            print('Pair found', (nums[d.get(target - e)], nums[i]))
            pair_found = True
            continue

        # store index of the current element in the dictionary
        d[e] = i
 
    # No pair with the given sum exists in the list
    if not pair_found:
        print('Pair not found')
 
 
if __name__ == '__main__':
 
    nums = [8, 7, 2, 5, 3, 1]
    target = 10
 
    findPair(nums, target)
 

