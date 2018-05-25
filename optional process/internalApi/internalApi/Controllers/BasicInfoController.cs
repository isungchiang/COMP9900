using Neo4j.Driver.V1;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Web.Http;

namespace internalApi.Controllers
{
    public class BasicInfoController : ApiController
    {
        private GraphDriver g;
        public void Init()
        {
            g = new GraphDriver();
        }

        [AcceptVerbs("GET", "POST")]
        [HttpGet]
        public HttpResponseMessage GetBasicInfo(string stockId)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(stockId))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output = String.Empty;
                string query = "MATCH(s:stock{StockId:\"" + stockId + "\"}) return s";
                Dictionary<string, string> nodes = new Dictionary<string, string>();
                IStatementResult StockResult = g.Write_and_return(query);
                foreach (IRecord record in StockResult)
                {
                    INode source = record["s"].As<INode>();

                    nodes = new Dictionary<string, string> {
                        {"StockId",source["StockId"].As<string>()},
                        {"Corporation",source["Corporation"].As<string>()},
                        {"Market",source["Market"].As<string>()},
                        {"Industry",source["Industry"].As<string>() },
                        {"Sector",source["Sector"].As<string>()},
                        {"Contact",source["Contact"].As<string>()},
                        {"Address",source["Address"].As<string>()},
                        {"EmployeesNum",source["EmployeesNum"].As<string>()},
                        { "Description",source["Description"].As<string>()},
                };

                }
                output = JsonConvert.SerializeObject(nodes);
                if (!string.IsNullOrEmpty(output))
                {
                    response.StatusCode = HttpStatusCode.OK;
                    response.Content = new StringContent(output, Encoding.UTF8);
                    response.Content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
                    return response;
                }
                else
                {
                    response.StatusCode = HttpStatusCode.NoContent;
                    return response;
                }
            }
            catch (Exception e)
            {
                response.StatusCode = HttpStatusCode.InternalServerError;
                response.Content = new StringContent(e.Message, Encoding.UTF8);
                return response;
            }
        }

        [AcceptVerbs("GET", "POST")]
        [HttpGet]
        public HttpResponseMessage GetNews(string stockId)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(stockId))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output = String.Empty;
                string query = "MATCH(:stock{StockId:\"" + stockId + "\"})-[]->(n:news) return n order by n.date DESC limit 100";
                List<Dictionary<string, string>> news = new List<Dictionary<string, string>>();
                IStatementResult StockResult = g.Write_and_return(query);
                foreach (IRecord record in StockResult)
                {
                    INode source = record["n"].As<INode>();

                    Dictionary<string, string> onenews = new Dictionary<string, string> {
                        {"StockId",source["StockId"].As<string>()},
                        {"date",source["date"].As<string>()},
                        {"mark",source["mark"].As<string>()},
                        {"title",source["title"].As<string>() },
                        {"relative",source["relative"].As<string>()},
                        {"url",source["url"].As<string>()} };
                    news.Add(onenews);    
                }
                output = JsonConvert.SerializeObject(news);
                if (!string.IsNullOrEmpty(output))
                {
                    response.StatusCode = HttpStatusCode.OK;
                    response.Content = new StringContent(output, Encoding.UTF8);
                    response.Content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
                    return response;
                }
                else
                {
                    response.StatusCode = HttpStatusCode.NoContent;
                    return response;
                }
            }
            catch (Exception e)
            {
                response.StatusCode = HttpStatusCode.InternalServerError;
                response.Content = new StringContent(e.Message, Encoding.UTF8);
                return response;
            }
        }

        [AcceptVerbs("GET", "POST")]
        [HttpGet]
        public HttpResponseMessage GetStat(string stockId)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(stockId))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output = String.Empty;
                string query = "MATCH(:stock{StockId:\"" + stockId + "\"})-[]->(n:stat) return n";
                List<Dictionary<string, string>> stat = new List<Dictionary<string, string>>();
                IStatementResult StockResult = g.Write_and_return(query);
                foreach (IRecord record in StockResult)
                {
                    INode source = record["n"].As<INode>();

                    Dictionary<string, string> onenews = new Dictionary<string, string> {
                        {"StockId",source["StockId"].As<string>()},
                        {"json",source["json"].As<string>()} };
                    stat.Add(onenews);
                }
                output = JsonConvert.SerializeObject(stat);
                if (!string.IsNullOrEmpty(output))
                {
                    response.StatusCode = HttpStatusCode.OK;
                    response.Content = new StringContent(output, Encoding.UTF8);
                    response.Content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
                    return response;
                }
                else
                {
                    response.StatusCode = HttpStatusCode.NoContent;
                    return response;
                }
            }
            catch (Exception e)
            {
                response.StatusCode = HttpStatusCode.InternalServerError;
                response.Content = new StringContent(e.Message, Encoding.UTF8);
                return response;
            }
        }
        [AcceptVerbs("GET", "POST")]
        [HttpGet]
        public HttpResponseMessage GetPerson(string stockId)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(stockId))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output = String.Empty;
                string query = "MATCH(:stock{StockId:\"" + stockId + "\"})-[]->(p:person) return p limit 15";
                List<Dictionary<string, string>> news = new List<Dictionary<string, string>>();
                IStatementResult StockResult = g.Write_and_return(query);
                foreach (IRecord record in StockResult)
                {
                    INode source = record["p"].As<INode>();

                    Dictionary<string, string> oneperson = new Dictionary<string, string> {
                        {"StockId",source["StockId"].As<string>()},
                        {"Name",source["Name"].As<string>()},
                        {"Position",source["Position"].As<string>()},
                        {"Age",source["Age"].As<string>()},
                        {"Since",source["Since"].As<string>() },
                        {"Description",source["Description"].As<string>()} };
                    news.Add(oneperson);
                }
                output = JsonConvert.SerializeObject(news);
                if (!string.IsNullOrEmpty(output))
                {
                    response.StatusCode = HttpStatusCode.OK;
                    response.Content = new StringContent(output, Encoding.UTF8);
                    response.Content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
                    return response;
                }
                else
                {
                    response.StatusCode = HttpStatusCode.NoContent;
                    return response;
                }
            }
            catch (Exception e)
            {
                response.StatusCode = HttpStatusCode.InternalServerError;
                response.Content = new StringContent(e.Message, Encoding.UTF8);
                return response;
            }
        }
    }
}
