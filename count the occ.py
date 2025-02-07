class Solution:
    
    #Function to find all elements in array that appear more than n/k times.
    def countOccurence(self,arr,n,k):
        count = {} # empty dictionary to store occurrence count of each element
        res = 0 # variable to store the count of elements appearing more than n/k times
        
        # iterating over the array
        for i in range(n):
            # if the element is not present in the dictionary, add it with count 1
            if arr[i] not in count:
                count[arr[i]] = 1
            # if the element is already present, increment its count by 1
            else:
                count[arr[i]] += 1
        
        # iterating over the dictionary
        for occurs in count:
            # if the occurrence of the element is more than n/k, increment the result count
            if count[occurs] > n // k:
                res += 1
        
        return res