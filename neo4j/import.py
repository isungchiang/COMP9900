from neo4j.v1 import GraphDatabase

URL = "bolt://52.237.192.182:7687"
USER = "neo4j"
PASSWORD = "cs9900Fafafa"

urlYahooProfile = 'https://raw.githubusercontent.com/isungchiang/cs9900PublicData/master/YahooProfile.csv'
urlReutersPeople = 'https://raw.githubusercontent.com/isungchiang/cs9900PublicData/master/ReutersPeople.csv'
class Graph(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_in_query(self, query):
        with self._driver.session() as session:
            session.run(query)

if __name__ == '__main__':
    g = Graph(URL, USER, PASSWORD)
    queryYahooProfile = "create (:stock{StockId:line.StockId," \
                        "Corporation:line.Corporation," \
                        "Market:line.Market," \
                        "Address:line.Address," \
                        "Contact:line.Contact," \
                        "Sector:line.Sector," \
                        "Industry:line.Industry," \
                        "EmployeesNum:line.EmployeesNum," \
                        "Description:line.Description" \
                        "})"
    queryReutersPeople = "create (:person{PersonId:line.PersonId," \
                         "StockId:line.StockId," \
                         "Name:line.Name," \
                         "Age:line.Age," \
                         "Since:line.Since," \
                         "Position:line.Position," \
                         "Description:line.Description" \
                         "})"
    INDEX_CREATE_Profile = "CREATE INDEX ON :stock(StockId)"
    INDEX_CREATE_People = "CREATE INDEX ON :person(PersonId)"
    queryStockPeople = "MATCh (s:stock{StockId:line.StockId}),(p:person{PersonId:line.PersonId}) " \
                       "create (s)-[:senior_executives]->(p) " \
                       "create (p)-[:senior_executives_of]->(s)"
    query_YahooProfile = "USING PERIODIC COMMIT " \
                   "LOAD CSV WITH HEADERS  FROM \"{0}\" AS line FIELDTERMINATOR '\t' {1}".format(urlYahooProfile,
                                                                                                 queryYahooProfile)
    query_ReutersPeople = "USING PERIODIC COMMIT " \
                         "LOAD CSV WITH HEADERS  FROM \"{0}\" AS line FIELDTERMINATOR '\t' {1}".format(urlReutersPeople,
                                                                                                       queryReutersPeople)
    query_StockPeople = "USING PERIODIC COMMIT " \
                      "LOAD CSV WITH HEADERS  FROM \"{0}\" AS line FIELDTERMINATOR '\t' {1}".format(urlReutersPeople,
                                                                                                    queryStockPeople)
    # g.add_in_query(query_YahooProfile)
    # g.add_in_query(query_ReutersPeople)
    # g.add_in_query(INDEX_CREATE_Profile)
    # g.add_in_query(INDEX_CREATE_People)
    g.add_in_query(query_StockPeople)