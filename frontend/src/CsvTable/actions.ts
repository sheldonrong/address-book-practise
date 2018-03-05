import * as request from 'superagent';

export const getAddressBooks = (
    callback: (e: any) => any,
    page: number,
    size: number,
) => {
    request
        .get('/api/address-book/')
        .query({'size': size})
        .query({'page': page})
        .then(callback);
};

export const getTotalPages = (
    pageSize: number,
    callback: (e: any) => any,
) => {
    request
        .get(`/api/address-book/metadata/${pageSize}`)
        .then(callback);
};
