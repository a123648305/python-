import time

def main():
    str = input("Enter the URL: ")



list = list(range(1,100))

# 二分查找
def search(list,target):
    i = 0
    j = len(list) - 1
    while i<=j:
        mid = (i+j)//2
        if list[mid] == target:
            return mid
        elif list[mid] > target:
            j = mid - 1
        else:
            i = mid + 1
    return -1

# 


start_time = time.time()

print(search(list,50))

print(f"---耗时 {time.time() - start_time} seconds ---")



# 快速排序
def quick_sort(list):
    if len(list) <= 1:
        return list
    pivot = list[0]
    left = [x for x in list[1:] if x < pivot]
    right = [x for x in list[1:] if x >= pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)


print(quick_sort([1,3,2,5,6,8,10,4]))



