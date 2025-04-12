# Exception class
class InvalidArrayLengthException(Exception):
    pass

# Exception class
class InvalidRunException(Exception):
    pass

def calcMinRun(n, run_size): 
    """Returns the minimum length of a run that ensures len(array)/minrun 
    is less than or equal to a power of 2."""
    r = 0
    while n >= run_size: 
        r |= n & 1
        n >>= 1
    return n + r 
  
  
def insertionSort(arr, left, right): 
    """Sorts array using insertion sort in the range [left, right]."""
    for i in range(left + 1, right + 1): 
        j = i 
        while j > left and arr[j] < arr[j - 1]: 
            arr[j], arr[j - 1] = arr[j - 1], arr[j] 
            j -= 1
  
  
def merge(arr, l, m, r): 
    """Merges two sorted subarrays of arr: [l..m] and [m+1..r]."""
    left = arr[l:m+1]
    right = arr[m+1:r+1]
    
    i, j, k = 0, 0, l 
    
    while i < len(left) and j < len(right): 
        if left[i] <= right[j]: 
            arr[k] = left[i] 
            i += 1
        else: 
            arr[k] = right[j] 
            j += 1
        k += 1
  
    # Copy remaining elements
    while i < len(left): 
        arr[k] = left[i] 
        i += 1
        k += 1
  
    while j < len(right): 
        arr[k] = right[j] 
        j += 1
        k += 1
  

def timSort(arr, array_len, run_size): 
    """TimSort with configurable run_size."""
    
    if run_size <= 0:
        raise InvalidRunException()
    
    if len(arr) != array_len:
        raise InvalidArrayLengthException()
    
    n = array_len
    minRun = calcMinRun(n, run_size)  # Use the configurable run_size
  
    # Sort individual subarrays of size minRun
    for start in range(0, n, minRun): 
        end = min(start + minRun - 1, n - 1) 
        insertionSort(arr, start, end) 
  
    size = minRun 
    while size < n: 
        for left in range(0, n, 2 * size): 
            mid = min(n - 1, left + size - 1) 
            right = min((left + 2 * size - 1), (n - 1)) 
            if mid < right: 
                merge(arr, left, mid, right) 
        size *= 2

    return arr