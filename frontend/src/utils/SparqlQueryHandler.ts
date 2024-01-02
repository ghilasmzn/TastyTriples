const SparqlClient = require('sparql-http-client');

interface QueryResult {
  on: (event: string, callback: (row: Record<string, any>) => void) => void;
}

class SparqlQueryHandler {
  private baseUrl: string;
  private updateUrl: string;
  private sparqlUrl: string;
  private client: any;

  constructor() {
    this.baseUrl = "http://localhost:3030/Coopcycle";
    this.updateUrl = `${this.baseUrl}/update`;
    this.sparqlUrl = `${this.baseUrl}/sparql`;

    this.client = new SparqlClient({
      endpointUrl: this.sparqlUrl,
      updateUrl: this.updateUrl,
    });
  }

  private formatRow(row: Record<string, any>): Record<string, any> {
    const formattedRow: Record<string, any> = {};
    Object.entries(row).forEach(([key, value]) => {
      formattedRow[key] = value.value;
    });
    return formattedRow;
  }

  private fetch(result: QueryResult): Promise<Record<string, any>[]> {
    return new Promise((resolve, reject) => {
      const rows: Record<string, any>[] = [];

      result.on("data", (rowOrError: Record<string, any> | Error) => {
        if (rowOrError instanceof Error) {
          reject(rowOrError);
        } else {
          rows.push(this.formatRow(rowOrError));
        }
      });

      result.on("end", () => {
        resolve(rows);
      });
    });
  }

  async exec(query: string): Promise<Record<string, any>[] | undefined> {
    try {
      const result: QueryResult = await this.client.query.select(query);
      const rows: Record<string, any>[] = await this.fetch(result);
      return rows;
    } catch (error) {
      console.error(error);
      return undefined;
    }
  }

  async construct(query: string): Promise<Record<string, any>[] | undefined> {
    try {
      const result: QueryResult = await this.client.query.construct(query);
      const rows: Record<string, any>[] = await this.fetch(result);
      return rows;
    } catch (error) {
      console.error(error);
      return undefined;
    }
  }

  async update(query: string): Promise<void> {
    try {
      await this.client.query.update(query);
      console.log("Update query executed successfully");
    } catch (error) {
      console.error(error);
    }
  }
}

export default SparqlQueryHandler;
