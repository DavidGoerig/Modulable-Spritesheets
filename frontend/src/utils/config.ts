// config.ts
import { ApiRoutes } from './apiRoutes';

export const API_BASE_URL = 'http://localhost:8090';


export class ApiConfig {
    static getFullUrl(route: ApiRoutes): string {
        return `${API_BASE_URL}${route}`;
    }
}