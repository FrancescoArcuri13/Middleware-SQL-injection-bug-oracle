import time
from testFile.pyTest.testSDU_MySQL import runTest
from testFile.tools import saveResult, estimate_completion_time, print_progress_bar, string_time, save_info

numberOfTests = 5000000

directory = "../testResult"  # Directory to save result

path_serverError = "../../serverError-(fuzzer).py"
path_Middleware = "../middleware.py"

path_generation = "../generate/mySQL-generate.py"

info_file = "/info_" + str(numberOfTests) + ".txt"

save_info(directory + info_file)

#Linux
#subprocess.run(["gnome-terminal", "--", "python3", path_serverError])
#subprocess.run(["gnome-terminal", "--", "python3", path_Middleware])

#Generate data
#subprocess.run(["gnome-terminal", "--", "python3", path_generation])

#subprocess.run(["/snap/pycharm-professional/368/bin/pycharm.sh", path_serverError])
#subprocess.run(["/snap/pycharm-professional/368/bin/pycharm.sh", path_Middleware])

#Windows
#subprocess.run(["start", "cmd", "/k", "python", path_serverError], shell=True)
#subprocess.run(["start", "cmd", "/k", "python", path_Middleware], shell=True)


# Phase 1 Tests time without Middleware
start = time.perf_counter()

# all_test_noProxy = []
#
# for i in range(numberOfTests):
#     test_execution = runTest(3306)
#     if len(test_execution) != 5: raise ValueError("List elements != 5")
#     all_test_noProxy.append(test_execution)
#     if i % 100 == 0:
#         print("noProxy:" + str(i))
#         remaining_time = estimate_completion_time(numberOfTests + numberOfTests - i, time.perf_counter()-start, i)
#         print("remaining_time: " + string_time(remaining_time))
#         print('********************')
#         print_progress_bar(2*numberOfTests, i)
#         print('\n********************')
#
# print("start saving result_noProxy_")
# saveResult(directory, all_test_noProxy, "result_noProxy_" + str(numberOfTests) + ".csv")
# print("saving finished result_noProxy_")
# time.sleep(5)
# start += 5

# Phase 2 Tests time with Middleware
all_test_Proxy = []  # Matrix with all test execution

for i in range(numberOfTests):
    test_execution = runTest(9092)
    if len(test_execution) != 5: raise ValueError("List elements != 5")
    all_test_Proxy.append(test_execution)
    if i % 100 == 0:
        print("Proxy:" + str(i))
        remaining_time = estimate_completion_time(numberOfTests - i, time.perf_counter()-start, i ) # + numberOfTests)
        print("remaining_time: " + string_time(remaining_time))
        print('********************')
        print_progress_bar(2*numberOfTests, numberOfTests + i)
        print('\n********************')

# Phase 3 save result in file
total_time = time.perf_counter() - start
print("time for 2*" + str(numberOfTests) + ": " + string_time(total_time))

with open(directory + info_file, "a") as file:
    file.write("\nTotal execution time\n")
    file.write("execution " + str(numberOfTests) + " times proxy and noProxy: " + string_time(total_time))

print("start saving result_Proxy_")
saveResult(directory, all_test_Proxy, "result_Proxy_" + str(numberOfTests) + ".csv")
print("saving finished result_Proxy_")

