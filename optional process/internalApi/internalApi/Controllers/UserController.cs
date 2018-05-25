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
    public class UserController : ApiController
    {
        private GraphDriver g;
        public void Init()
        {
            g = new GraphDriver();
        }

        [AcceptVerbs("GET", "POST")]
        [HttpGet]
        public HttpResponseMessage Register(string username, string password)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(username)||string.IsNullOrEmpty(password))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output;
                Dictionary<string, string> outict = new Dictionary<string, string>();
                string query = "MATCH(u:user{username:\"" + username + "\"}) return u";
                IStatementResult SearchResult = g.Write_and_return(query);
                Boolean already_exist = false;
                foreach (IRecord record in SearchResult)
                {
                    already_exist = true;
                }
                if (!already_exist)
                {
                    string create_new_user = "create (u:user{username:\"" + username + "\",password:\"" + password + "\"}) " +
                        "create (p:portfolio{name:\"Watchlist\",username:\""+username + "\"}) " +
                        "create (u)-[:hasportfolio]->(p)";
                    g.Write_and_return(create_new_user);
                }
                outict.Add("Create User Status", already_exist ? "Fail" : "Success");
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
        public HttpResponseMessage Login(string username, string password)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output;
                Dictionary<string, string> outict = new Dictionary<string, string>();
                string query = "MATCH(u:user{username:\"" + username + "\",password:\"" + password + "\"}) return u";
                IStatementResult SearchResult = g.Write_and_return(query);
                Boolean already_exist = false;
                foreach (IRecord record in SearchResult)
                {
                    already_exist = true;
                }
                outict.Add("Login Status", already_exist ? "Success" : "Fail");
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
        public HttpResponseMessage GetUserProfile(string username)
        {
            var response = Request.CreateResponse();
            response.Headers.Add("Access-Control-Allow-Origin", "*");
            try
            {
                if (string.IsNullOrEmpty(username))
                {
                    response.StatusCode = HttpStatusCode.BadRequest;
                    return response;
                }
                Init();
                string output;

                Dictionary<string, List<Dictionary<string, string>>> outict = new Dictionary<string, List<Dictionary<string, string>>>();
                string query1 = "MATCH(u:user{username:\"" + username + "\"})-[]-(p) return p";
                string query2 = "MATCH(u:user{username:\"" + username + "\"})-[]-()-[r]-() return r";
                IStatementResult SearchResult1 = g.Write_and_return(query1);
                IStatementResult SearchResult2 = g.Write_and_return(query2);
                foreach (IRecord record in SearchResult1)
                {
                    INode portfolio1 = record["p"].As<INode>();

                    if (!outict.ContainsKey(portfolio1["name"].As<string>()))
                    {
                        outict.Add(portfolio1["name"].As<string>(), new List<Dictionary<string, string>>());
                    }

                }
                foreach (IRecord record in SearchResult2)
                {
                    IRelationship relation = record["r"].As<IRelationship>();
                    Dictionary<string, string> tmp = new Dictionary<string, string>
                {
                    { "StockId",relation["StockId"].As<string>() },
                    { "Shares",relation["Shares"].As<string>() },
                    { "TradeDate",relation["TradeDate"].As<string>() },
                    { "TradePrice",relation["TradePrice"].As<string>() }
                };
                    if (!outict.ContainsKey(relation["portfolioname"].As<string>()))
                    {
                        outict.Add(relation["portfolioname"].As<string>(), new List<Dictionary<string, string>> { tmp });
                    }
                    else
                    {
                        outict[relation["portfolioname"].As<string>()].Add(tmp);
                    }
                }
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
