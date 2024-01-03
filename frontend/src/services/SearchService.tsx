import SparqlQueryHandler from "../utils/SparqlQueryHandler";

class SearchService {
  private queryHandler: SparqlQueryHandler;

  constructor() {
    this.queryHandler = new SparqlQueryHandler();
  }

  private parseResults(data: any[]): any[] {
    data.forEach((result: any) => {
      Object.keys(result).forEach((key: string) => {
        const value = result[key];
        if (value.type === 'literal') {
          result[key] = value.value;
        }
      });
    });

    return data;
  }
  
  private async search(query: string) {
    return await this.queryHandler.select(query);
  }

  public async searchRestaurants(keywords: string): Promise<any[] | undefined> {
    const query = `
          PREFIX ns1: <http://schema.org/>

          SELECT ?restaurant ?name ?description ?image ?streetAddress ?telephone
          WHERE {
            ?restaurant a ns1:Restaurant ;
                        ns1:name ?name ;
                        ns1:description ?description ;
                        ns1:image ?image ;
                        ns1:address ?address .

            ?address ns1:name ?addressName ;
                    ns1:streetAddress ?streetAddress ;
                    ns1:geo ?geo ;
                    ns1:telephone ?telephone .

            FILTER(
              regex(str(?name), "${keywords}", "i") || 
              regex(str(?description), "${keywords}", "i")
            )
          }
    `;

    const result = await this.search(query);
    return result;
  }

}

export default SearchService;
