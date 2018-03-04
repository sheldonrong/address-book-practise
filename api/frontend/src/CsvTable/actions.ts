import { fetch } from '../utils';

export const getAddressBooks = (callback: Function) => {
    fetch('/api/address-book/', callback);
};