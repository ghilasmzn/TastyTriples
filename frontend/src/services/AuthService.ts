import SparqlQueryHandler from '../utils/SparqlQueryHandler';

interface AuthService {
  login: (email: string, password: string) => Promise<boolean>;
  signup: (email: string, password: string) => Promise<boolean>;
}

const AuthService: AuthService = {
    login: async (email: string, password: string) => {
      try {
        const sparqlClient = new SparqlQueryHandler(); 

        const loginQuery = `
          PREFIX schema: <http://schema.org/>
          PREFIX ex: <http://example.com/ontology#>

          SELECT ?user ?email ?password 
          FROM <http://localhost:3030/Coopcycle/users>
          WHERE {
            ?user a schema:Person ;
                    schema:email "${email}" ;
                    ex:password "${password}" .
          }
        `;

        const result = await sparqlClient.exec(loginQuery);
        return result !== undefined && result.length > 0;
      } catch (error) {
        console.error('Error during login:', error);
        return false;
      }
    },
  
  signup: async (email: string, password: string) => {
    try {
      const sparqlClient = new SparqlQueryHandler();
  
      // Construct the SPARQL query to insert a new user
      const signupQuery = `
            PREFIX ex: <http://example.com/ontology#>
            PREFIX schema: <http://schema.org/>

            INSERT DATA {
              GRAPH <http://localhost:3030/Coopcycle/users> {
                _:user a schema:Person ;
                  schema:email "${email}" ;
                  ex:password "${password}" .
              }
            }
      `;
  
      await sparqlClient.update(signupQuery);
      return true;
    } catch (error) {
      console.error('Error during signup:', error);
      return false;
    }
  },
  
};

export default AuthService;
