import sys, os, subprocess
def error(msg):
    print("\033[91;1merror:\033[0m " + msg)
try:
    version = subprocess.check_output(["rbxtsc", "--version"]).decode("utf-8").strip()
except FileNotFoundError:
    error("rbxtsc not found!")
    sys.exit(1)
args = sys.argv[1:]
flags = []
inputf = []
outputf = None
lookForOutput = False
for arg in args:
    if arg == "-o":
        lookForOutput = True
    elif arg.startswith("-"):
        flags.append(arg)
    elif lookForOutput:
        outputf = arg
        lookForOutput = False
    else:
        inputf.append(arg)
if inputf is []:
    error("no input file")
    sys.exit(1)
elif len(inputf) > 1:
    error("too many input files")
    sys.exit(1)
else:
    inputf = inputf[0]
if outputf is None:
    error("no output file")
    sys.exit(1)
tsCode = open(inputf, "r").read()
if not os.path.exists("qtstemp"):
    subprocess.run(["git", "clone", "--depth=1", "https://github.com/AsynchronousAI/qtstemp.git"], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
file = open("qtstemp/src/index.server.ts", "w")
file.write(tsCode)
file.close()
for i, v in enumerate(flags):
    if v.startswith("-I"):
        install = v[2:]
        subprocess.run(["npm", "install", install], cwd = "qtstemp")
        path = "qtstemp/node_modules/" + install
        luaFiles = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".lua"):
                    luaFiles.append([os.path.join(root, file), file])
        for file in luaFiles:
            contents = open(file[0], "r").read()
            requiredDirs = os.path.join("include", install, file[1]).split("/")
            for i in range(len(requiredDirs) - 1):
                dir = "/".join(requiredDirs[:i + 1])
                if not os.path.exists(dir):
                    os.mkdir(dir)
            file = open(os.path.join("include", install, file[1]), "w+")
            file.write(contents)
            file.close()
            
subprocess.run(["rbxtsc"], cwd = "qtstemp")
runtimeLib = open("qtstemp/include/RuntimeLib.lua", "r").read()
luaCode = open("qtstemp/out/init.server.lua", "r").read()
file = open(outputf, "w")
file.write(luaCode)
file.close()
file = open("runtime.lua", "w+")
file.write(runtimeLib)
file.close()
if "-k" not in flags:
    subprocess.run(["rm", "-rf", "qtstemp"])
