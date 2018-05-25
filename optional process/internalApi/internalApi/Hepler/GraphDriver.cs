using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Neo4j.Driver.V1;

namespace internalApi
{
    public class GraphDriver : IDisposable
    {
        private readonly IDriver _driver;
        public GraphDriver(string url = @"bolt://23.101.218.173:7687",
            string user = "neo4j", string password = "Cs9900fafafa")
        {
            _driver = GraphDatabase.Driver(url, AuthTokens.Basic(user, password));
        }
        public IStatementResult Write_and_return(string query)
        {
            using (var session = _driver.Session())
            {
                var query_result = session.WriteTransaction(tx =>
                {
                    var result = tx.Run(query);
                    return result;
                });
                return query_result;
            }
        }
        public void Dispose()
        {
            _driver?.Dispose();
        }
    }
}
