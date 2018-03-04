import * as request from 'superagent';
import { ImageFile } from 'react-dropzone';

export const upload = (
    file: ImageFile,
    onProgress: (e: any) => any,
    onError: (e: any) => any,
    callback: (e: any) => any,
) => {
    request
        .post('/upload')
        .attach('file', file)
        .on('progress', onProgress)
        .on('error', onError)
        .then(callback);
};

export const getFileInfo = (
    fileHash: string,
    onSuccess: (e: any) => any,
    onError: (e: any) => any,
    encoding?: string,
    delimiter?: string,
    hasHeader?: boolean,
    quotechar?: string
) => {
    request
        .get(`api/csv/${fileHash}`)
        .query({'encoding': encoding})
        .query({'delimiter': delimiter})
        .query({'quotechar': quotechar})
        .query(hasHeader != null ? {'has_header': Number(hasHeader)} : {})
        .on('error', onError)
        .then(onSuccess);
};

export const importAddressBook = (
    fileHash: string,
    encoding: string,
    delimiter: string,
    hasHeader: boolean,
    quotechar: string,
    resolveConflicts: string,
    onSuccess: (e: any) => any,
    onError: (e: any) => any,
) => {
    request
        .post('api/address-book/import')
        .send({
            file_hash: fileHash,
            metadata: {
                encoding: encoding,
                delimiter: delimiter,
                has_header: Number(hasHeader),
                quotechar: quotechar
            },
            resolve_conflicts: resolveConflicts
        })
        .on('error', onError)
        .then(onSuccess);
};