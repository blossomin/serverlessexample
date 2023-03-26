import json

def lambda_handler(event, context):
    arr = event['array']
    sorted_arr = quicksort(arr)
    response = {
        'sorted_array': sorted_arr
    }
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
