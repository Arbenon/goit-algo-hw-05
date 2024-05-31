def binary_search(arr, x):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        if arr[mid] == x:
            return (iterations, arr[mid])
        elif arr[mid] < x:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1
    
    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]
    
    return (iterations, upper_bound)

# Тест
sorted_array = [1.1, 3.1, 4.5, 6.6, 1.7, 12.5, 3.1, 2.2, 3.3, 4.4, 5.5]
value_to_find = 3.0

result = binary_search(sorted_array, value_to_find)
print(result)
