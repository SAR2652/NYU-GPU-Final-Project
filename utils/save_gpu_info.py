from utils import GPUProfiler, ParseTreeGenerator

def getGPUDetails():
    gpu = GPUProfiler()
    # print(gpu.getDevicePropDict())
    # print(gpu.getDevicePropJSON())
    gpu.saveAsJSON()

def generateParseTree(filename: str):
    ptg = ParseTreeGenerator(filename)
    print(ptg.getParseTreeString())
    ptg.saveParseTreeText()

# generateParseTree(sys.argv[1])
getGPUDetails()