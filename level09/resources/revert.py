to_revert =  "102 52 107 109 109 54 112 124 61 130 127 112 130 110 131 130 68 66 131 68 117 123 127 140 137"

revert_list = to_revert.split(" ")
res = ""
for i, x in enumerate(revert_list):
	res += chr(int(x) - i)
print(res)
