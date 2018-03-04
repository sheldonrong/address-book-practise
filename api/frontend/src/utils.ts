export const fetch = (url: string, callback: Function, options?: any) => {
    (window as any).fetch(url).then((response: any) => response.json()).then((result: any) => callback(result));
};