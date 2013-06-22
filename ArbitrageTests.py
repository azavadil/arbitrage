import Arbitrage



testData1 = dict([('USD_JPY', 111.3040336),('USD_BTC', 0.0090186),('USD_EUR', 0.8450542),('USD_USD', 1.0), \
                   ('JPY_EUR', 0.0069366),('JPY_BTC', 7.41e-05),('JPY_USD', 0.0089169),('JPY_JPY', 1.0),    \
                   ('EUR_USD', 1.1438212),('EUR_JPY', 117.1936805),('EUR_BTC', 0.0100144),('EUR_EUR', 1.0), \
                   ('BTC_JPY', 13688.9099566),('BTC_USD', 133.724882),('BTC_EUR', 98.6388682),('BTC_BTC', 1.0),])

testData2 = dict([('USD_JPY', 111.3040336),('USD_BTC', 0.0090186),('USD_EUR', 0.8450542),('USD_USD', 1.0), \
                  ('JPY_USD', 0.0089844),('JPY_EUR', 0.0069366),('JPY_BTC', 7.41e-05),('JPY_JPY', 1.0), \
                  ('EUR_JPY', 117.1936805),('EUR_USD', 1.1438212),('EUR_BTC', 0.0100144),('EUR_EUR', 1.0), \
                 ('BTC_JPY', 13495.27665),('BTC_USD',110.8819551),('BTC_EUR', 98.6388682),('BTC_BTC', 1.0)])

testData3 = dict([('USD_JPY', 1),('USD_BTC', 1),('USD_EUR', 1),('USD_USD', 1.0), \
                  ('JPY_USD', 1),('JPY_EUR', 1),('JPY_BTC', 1),('JPY_JPY', 1.0), \
                  ('EUR_JPY', 1),('EUR_USD', 1),('EUR_BTC', 1),('EUR_EUR', 1.0), \
                 ('BTC_JPY', 1),('BTC_USD',1),('BTC_EUR', 1),('BTC_BTC', 1.0)])

testData4 = dict([('USD_EUR', 0.741), ('USD_GBP', 0.657), ('USD_CHF', 1.061), ('USD_CAD', 1.011), \
                 ('EUR_USD', 1.350), ('EUR_GBP', 0.888), ('EUR_CHF', 1.432), ('EUR_CAD', 1.366), \
                 ('GBP_USD', 1.521), ('GBP_EUR', 1.126), ('GBP_CHF', 1.610), ('GBP_CAD', 1.538), \
                 ('CHF_USD', 0.943), ('CHF_EUR', 0.697), ('CHF_GBP', 0.620), ('CHF_CAD', 0.953), \
                 ('CAD_USD', 0.995), ('CAD_EUR', 0.732), ('CAD_GBP', 0.650), ('CAD_CHF', 1.049)])
            
testData5 = dict([('USD_EUR', 0.741), ('USD_GBP', 0.657), ('USD_CHF', 1.061), ('USD_CAD', 1.004), \
                 ('EUR_USD', 1.340), ('EUR_GBP', 0.886), ('EUR_CHF', 1.430), ('EUR_CAD', 1.366), \
                 ('GBP_USD', 1.521), ('GBP_EUR', 1.126), ('GBP_CHF', 1.610), ('GBP_CAD', 1.538), \
                 ('CHF_USD', 0.943), ('CHF_EUR', 0.697), ('CHF_GBP', 0.620), ('CHF_CAD', 0.953), \
                 ('CAD_USD', 0.995), ('CAD_EUR', 0.732), ('CAD_GBP', 0.650), ('CAD_CHF', 1.049)])

            

def testGraph():
    
    G = Arbitrage.makeGraph(testData)
    print G

def testIO():
    f = open('tinyG.txt', 'r')
    tinyG = list(f)
    tinyG = map(lambda x: x.strip(), tinyG)

    G = Arbitrage.WgtGraph()

    
    for line in tinyG:
        line = line.split()
        G.addEdge(arbitrage.DirectedEdge(line[0],line[1],float(line[2])))

    print G
    res = Arbitrage.WgtDirectedCycle(G)
    for edge in res.cycle():
        print edge

def testDictionaryBuild():
    
    csvReader = Arbitrage.makeFile()
    print Arbitrage.convertToDictionary(csvReader)


def mainTest(testData):
        
    G = Arbitrage.makeGraph(testData)
    
    bf = Arbitrage.BellmanFord(G, G.vertices()[0])

    if bf.hasNegativeCycle():
        result = bf.getCycle()
        print "Start with 100 units {0}".format(result[-1].fromVertex())
        balance = 100
        while result:
            edge = result.pop()
            key = edge.fromVertex() + "_" + edge.toVertex()
            balance = balance * testData[key]
            print "{0} to {1} @ {2} = {3:.2f} {4}".format(edge.fromVertex(), edge.toVertex(), testData[key], balance, edge.toVertex())
    else:
        print "No arbitrage found"
    print "\n"

def allTests():
	mainTest(testData1)
	mainTest(testData2)
	mainTest(testData3)
	mainTest(testData4)
	mainTest(testData5)
	

