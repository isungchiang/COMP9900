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
    public class PortfolioController : ApiController
    {
        private GraphDriver g;
        public void Init()
        {
            g = new GraphDriver();
        }

        [AcceptVerbs("GET", "POST")]
        [HttpGet]
        public HttpResponseMessage AddPortfolio(string username, string portfolioname)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(portfolioname))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output;
                Dictionary<string, string> outict = new Dictionary<string, string>();
                string query = "MATCH(p:portfolio{username:\"" + username + "\",name:\"" + portfolioname + "\"}) return p";
                IStatementResult SearchResult = g.Write_and_return(query);
                Boolean already_exist = false;
                foreach (IRecord record in SearchResult)
                {
                    already_exist = true;
                }
                if (!already_exist)
                {
                    string create_new_user = "Match (u:user{username:\"" + username + "\"}) " +
                        "create (p:portfolio{name:\"" + portfolioname + "\",username:\"" + username + "\"}) " +
                        "create (u)-[:hasportfolio]->(p)";
                    g.Write_and_return(create_new_user);
                }
                outict.Add("Create portfolio Status", already_exist ? "Fail" : "Success");
                output = JsonConvert.SerializeObject(outict);
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
        public HttpResponseMessage DeletePortfolio(string username, string portfolioname) {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(portfolioname))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output;
                Dictionary<string, string> outict = new Dictionary<string, string>();
                string query = "MATCH(p:portfolio{username:\"" + username + "\",name:\"" + portfolioname + "\"}) return p";
                IStatementResult SearchResult = g.Write_and_return(query);
                Boolean already_exist = false;
                foreach (IRecord record in SearchResult)
                {
                    already_exist = true;
                }
                if (already_exist)
                {
                    string create_new_user = "Match (p:portfolio{name:\"" + portfolioname + "\",username:\"" + username + "\"}) " +
                        "DETACH DELETE p";
                    g.Write_and_return(create_new_user);
                }
                outict.Add("Delete portfolio Status", already_exist ? "Success" : "Fail");
                output = JsonConvert.SerializeObject(outict);
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
        public HttpResponseMessage CreateTransaction(string username, string portfolioname, string StockId, string Shares, string TradeDate, string TradePrice)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(portfolioname) || string.IsNullOrEmpty(StockId))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output;
                Dictionary<string, string> outict = new Dictionary<string, string>();
                string query = "MATCH(s:stock{StockId:\"" + StockId + "\"}) return s";
                IStatementResult SearchResult = g.Write_and_return(query);
                Boolean already_exist = false;
                foreach (IRecord record in SearchResult)
                {
                    already_exist = true;
                }
                if (already_exist)
                {
                    string create_new_transaction = "MATCH(p:portfolio{username:\"" + username + "\",name:\"" + portfolioname + "\"}) " +
                        "MATCH(s:stock{StockId:\"" + StockId + "\"}) " +
                        "create (p)-[:hastransaction{StockId:\"" + StockId + "\",portfolioname:\""+portfolioname + "\",Shares:\"" + Shares + "\",TradeDate:\"" 
                        + TradeDate + "\", TradePrice:\"" + TradePrice + "\"}]->(s)";
                    g.Write_and_return(create_new_transaction);
                }
                outict.Add("Create Transaction Status", already_exist ? "Success" : "No Such Stock");
                output = JsonConvert.SerializeObject(outict);
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
        public HttpResponseMessage DeleteTransaction(string username, string portfolioname, string StockId, string Shares, string TradeDate, string TradePrice)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(portfolioname) || string.IsNullOrEmpty(StockId))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output;
                Dictionary<string, string> outict = new Dictionary<string, string>();
                string query = "MATCH(p:portfolio{username:\"" + username + "\",name:\"" + portfolioname + "\"}) " +
                        "MATCH(s:stock{StockId:\"" + StockId + "\"}) " +
                        "MATCH (p)-[r:hastransaction{StockId:\"" + StockId + "\",portfolioname:\"" + portfolioname + "\",Shares:\"" + Shares + "\",TradeDate:\""
                        + TradeDate + "\", TradePrice:\"" + TradePrice + "\"}]->(s) Delete r";
                IStatementResult SearchResult = g.Write_and_return(query);
                outict.Add("Create Transaction Status", "Success");
                output = JsonConvert.SerializeObject(outict);
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
