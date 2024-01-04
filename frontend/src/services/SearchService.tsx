import SparqlQueryHandler from "../utils/SparqlQueryHandler";

class SearchService {
  private queryHandler: SparqlQueryHandler;

  constructor() {
    this.queryHandler = new SparqlQueryHandler();
  }

  private async search(query: string) {
    return await this.queryHandler.select(query);
  }

  public async withFilters(location: string, distance: number, days: string[], minPrice: number, maxPrice: number, sortByPrice: boolean): Promise<any[] | undefined> {
    let dayHaving = '';
    if (days.length > 0) {
      const daysContainer: string[] = [];
      days.forEach(day => {
        daysContainer.push(`CONTAINS(GROUP_CONCAT(DISTINCT ?dayOfWeek; SEPARATOR=","), "${day}")`);
      });
      dayHaving = `HAVING (${daysContainer.join(' && ')})`;
    }

    let priceFilter = '';
    if (maxPrice > 0) {
      priceFilter = `FILTER (xsd:float(?price) >= ${minPrice} && xsd:float(?price) <= ${maxPrice})`;
    }

    let orderBy = '';
    if (sortByPrice) {
      orderBy = 'ORDER BY xsd:float(?price)';
    }

    let query = `
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ns1: <http://schema.org/>

        SELECT ?restaurant ?name ?description ?image ?streetAddress ?telephone ?price ?latitude ?longitude
              (GROUP_CONCAT(DISTINCT ?dayOfWeek; SEPARATOR=",") AS ?openDays)
        WHERE {
          ?restaurant a ns1:Restaurant ;
            ns1:name ?name ;
            ns1:description ?description ;
            ns1:image ?image ;
            ns1:address/ns1:streetAddress ?streetAddress ;
            ns1:address/ns1:telephone ?telephone ;
            ns1:address/ns1:geo/ns1:latitude ?latitude ;
            ns1:address/ns1:geo/ns1:longitude ?longitude .

          # Price filter
          OPTIONAL {
            ?restaurant ns1:potentialAction/ns1:priceSpecification/ns1:price ?price .
          }
          
          ${priceFilter}

          OPTIONAL {
            ?restaurant ns1:openingHoursSpecification [
              ns1:dayOfWeek ?dayOfWeek ;
              ns1:opens ?opens ;
              ns1:closes ?closes
            ]
          }
        }
        GROUP BY ?restaurant ?name ?description ?image ?streetAddress ?telephone ?price ?latitude ?longitude
        ${dayHaving}
        ${orderBy}
    `;

    console.log(query);

    const result = await this.search(query);
    return result;
  }

  public async byId(id: string): Promise<any | undefined> {
    const query = `
          PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
          PREFIX ns1: <http://schema.org/>

          SELECT ?restaurant ?name ?description ?image ?streetAddress ?telephone ?price ?latitude ?longitude ?network ?serviceUri ?serviceName ?serviceCity ?serviceCountry ?serviceDescription ?serviceMail
          (GROUP_CONCAT(DISTINCT CONCAT(?dayOfWeek, ": ", ?opens, "-", ?closes); SEPARATOR=", ") AS ?openingHours)
          (GROUP_CONCAT(DISTINCT ?serviceNetwork; SEPARATOR=", ") AS ?servicesNetwork)
          WHERE {
            ?restaurant a ns1:Restaurant ;
                        ns1:name ?name ;
                        ns1:description ?description ;
                        ns1:image ?image ;
                        ns1:address/ns1:streetAddress ?streetAddress ;
                        ns1:address/ns1:telephone ?telephone ;
                        ns1:address/ns1:geo/ns1:latitude ?latitude ;
                        ns1:address/ns1:geo/ns1:longitude ?longitude ;
                        ns1:belongsToService ?serviceUri .

            OPTIONAL {
              ?restaurant ns1:openingHoursSpecification [
                  ns1:dayOfWeek ?dayOfWeek ;
                  ns1:opens ?opens ;
                  ns1:closes ?closes
              ] 
            }

            OPTIONAL {
              ?restaurant ns1:sameAs ?network .
            }

            OPTIONAL {
              ?restaurant ns1:potentialAction/ns1:priceSpecification/ns1:price ?price .
            }

            # Service details
            ?serviceUri a ns1:ProfessionalService ;
                        ns1:name ?serviceName ;
                        ns1:city ?serviceCity ;
                        ns1:country ?serviceCountry ;
                        OPTIONAL { 
              ?serviceUri ns1:description ?descEN 
              FILTER(LANG(?descEN) = 'en')
            }

            OPTIONAL { 
              ?serviceUri ns1:description ?otherDesc 
              FILTER(LANG(?otherDesc) != 'en')
            }

            OPTIONAL {
              ?serviceUri ns1:sameAs ?serviceNetwork .
            }

            BIND(COALESCE(?descEN, ?otherDesc) AS ?serviceDescription)
            ?serviceUri ns1:mail ?serviceMail .

            FILTER (?restaurant = <${id}>)
          }
          GROUP BY ?restaurant ?name ?description ?image ?streetAddress ?telephone ?price ?latitude ?longitude ?network ?serviceUri ?serviceName ?serviceCity ?serviceCountry ?serviceDescription ?serviceMail
    `;

    const result = await this.search(query);
    return result?.length ? (result[0] as Record<string, any>) : undefined;
  }

  public async byName(keywords: string): Promise<any[] | undefined> {
    const query = `
          PREFIX ns1: <http://schema.org/>

          SELECT ?restaurant ?name ?description ?image ?streetAddress ?telephone ?price
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
          
            OPTIONAL {
              ?restaurant ns1:potentialAction/ns1:priceSpecification/ns1:price ?price .
            }

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
