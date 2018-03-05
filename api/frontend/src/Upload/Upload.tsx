import * as React from 'react';
import { Button, Modal, Progress, Icon, Form, DropdownProps, Message } from 'semantic-ui-react';
import Dropzone, { ImageFile } from 'react-dropzone';
import { upload, getFileInfo, importAddressBook } from './actions';
import { AddressBook, CsvTable } from 'CsvTable';

type UploadProps = {};

type FileInfo = {
    sampleData: Array<AddressBook>,
    delimiter?: string,
    quotechar?: string,
    encoding?: string,
    hasHeader?: boolean,
};

type UploadState = {
    confirmLoading: boolean,
    errorMessage: string,
    hasError: boolean,
    percent: number,
    uploadedFile: string,
    showProgress: boolean,
    fileInfo: FileInfo,
    modalOpen: boolean,
    resolveConflicts: string,
};

export class Upload extends React.Component<UploadProps, UploadState> {

    encodingOptions = [
        { key: 'utf-8', text: 'UTF-8', value: 'utf-8' },
        { key: 'utf-16', text: 'UTF-16', value: 'utf-16' },
        { key: 'ascii', text: 'ASCII', value: 'ascii' },
        { key: 'cp1250', text: 'Windows (CP1250)', value: 'cp1250' },
        { key: 'cp1251', text: 'Windows (CP1251)', value: 'cp1251' },
        { key: 'cp1252', text: 'Windows (CP1252)', value: 'cp1252' },
        { key: 'gbk', text: 'Chinese (GBK)', value: 'gbk' },
    ];

    delimiterOptions = [
        { key: 'space', text: 'Space ( )', value: ' ' },
        { key: 'semicolon', text: 'Semicolon (;)', value: ';' },
        { key: 'colon', text: 'Colon (:)', value: ':' },
        { key: 'comma', text: 'Comma (,)', value: ',' },
        { key: 'vertical-line', text: 'Vertical Line (|)', value: '|' },
    ];

    constructor(props: UploadProps) {
        super(props);
        this.state = {
            confirmLoading: false,
            errorMessage: '',
            hasError: false,
            percent: 0,
            modalOpen: false,
            showProgress: false,
            uploadedFile: '',
            fileInfo: {
                sampleData: []
            },
            resolveConflicts: 'keep_existing'
        };
    }

    getFileInfo = () => {
        getFileInfo(
            this.state.uploadedFile, 
            (r: any) => {
            this.setState({
                ...this.state,
                hasError: false,
                errorMessage: '',
                fileInfo: {
                    sampleData: r.body.sample_data,
                    delimiter: r.body.delimiter,
                    encoding: r.body.encoding,
                    hasHeader: r.body.has_header,
                    quotechar: r.body.quotechar
                }
                });
            },
            (e: any) => {
                this.setState({
                    ...this.state,
                    hasError: true,
                    errorMessage: e.response.body.message,
                    fileInfo: {
                        ...this.state.fileInfo,
                        sampleData: [],
                    }
                });
            },
            this.state.fileInfo.encoding,
            this.state.fileInfo.delimiter,
            this.state.fileInfo.hasHeader,
            this.state.fileInfo.quotechar,
        );
    }

    onDrop = (acceptedFiles: ImageFile[], rejectedFiles: ImageFile[]) => {
        if (!acceptedFiles) {
            this.setState({
                ...this.state,
                percent: 0,
                uploadedFile: ''
            });
        } else {
            upload(acceptedFiles[0], (e: any) => {
                    this.setState({
                        ...this.state,
                        percent: e.percent,
                        showProgress: true,
                        hasError: false,
                        errorMessage: ''
                    });
                }, (error: any) => {
                    this.setState({
                        ...this.state,
                        uploadedFile: '',
                        showProgress: false,
                        percent: 0,
                        hasError: true,
                        errorMessage: error.response.body.message
                    });
                }, (result: any) => {
                if (result.body && result.body.success) {
                    this.setState({
                        ...this.state,
                        uploadedFile: result.body.file,
                    },            this.getFileInfo);
                }
            });
        }
    }

    onClose = (e: any) => {
        this.setState({
            ...this.state,
            percent: 0,
            uploadedFile: '',
            showProgress: false,
            modalOpen: false,
        });
    }

    onOpen = (e: any) => {
        this.setState({
            ...this.state,
            hasError: false,
            percent: 0,
            modalOpen: true,
            showProgress: false,
            uploadedFile: '',
            fileInfo: {
                sampleData: []
            }
        });
    }

    onConfirm = (e: any) => {
        this.setState({
            ...this.state,
            confirmLoading: true
        });
        importAddressBook(
            this.state.uploadedFile,
            this.state.fileInfo.encoding || 'utf-8',
            this.state.fileInfo.delimiter || ' ',
            this.state.fileInfo.hasHeader || true,
            this.state.fileInfo.quotechar || '',
            this.state.resolveConflicts,
            (result: any) => {
                this.setState({
                    ...this.state,
                    confirmLoading: false,
                    modalOpen: false,
                });
            },
            (err: any) => {
                this.setState({
                    ...this.state,
                    confirmLoading: false,
                    modalOpen: false,
                    hasError: true,
                    errorMessage: `${err.response.body.message} (
                        ${Object.keys(err.response.body.errors).map((key => err.response.body.errors[key]))})`
                });
            }
        );
    }

    render() {
        return (
            <Modal
                trigger={
                    <Button className="upload" onClick={this.onOpen} color="facebook"> 
                        <Icon name="upload" /> Upload
                    </Button>}
                dimmer="blurring"
                style={{marginTop: '120px !important', margin: '120px auto'}}
                onClose={this.onClose}
                open={this.state.modalOpen}
                closeOnDimmerClick={false}
                closeOnEscape={false}
                closeOnDocumentClick={false}
            >
                <Modal.Header>Upload CSV File</Modal.Header>
                <Modal.Content>
                    <Message negative hidden={!this.state.hasError}>
                        <Message.Header>Oops</Message.Header>
                        <p>{this.state.errorMessage}</p>
                    </Message>
                    <Modal.Content>
                        <Dropzone className="drop-zone"
                            onDrop={this.onDrop}
                            style={{width: '100%'}}
                            maxSize={5242880} // 5MB
                            multiple={false}
                            disablePreview
                            accept="text/plain, text/csv"
                        >
                            <div>Click or Drop your CSV file here</div>
                            {this.state.showProgress &&
                            <Progress size="tiny" percent={this.state.percent} success/>}
                        </Dropzone>
                        {this.state.fileInfo && this.state.fileInfo.encoding &&
                        <Form>
                            <Form.Group widths="equal">
                                <Form.Select fluid required label="Encoding" 
                                    options={this.encodingOptions}
                                    placeholder="Choose a encoding"
                                    value={this.state.fileInfo.encoding}
                                    onChange={this.onEncodingChange}
                                />
                                <Form.Select fluid required label="Delimiter"
                                    options={this.delimiterOptions}
                                    placeholder="Choose a delimiter"
                                    value={this.state.fileInfo.delimiter}
                                    onChange={this.onDelimiterChange}
                                />
                            </Form.Group>
                            <Form.Group widths="equal">
                                <Form.Select fluid required label="Quote character"
                                    options={[
                                        {'key': 0, text: 'Not used', value: ' '},
                                        {'key': 1, text: 'Double quote ( " )', value: '"'},
                                        {'key': 2, text: 'Single quote ( \' )', value: '\''},
                                    ]}
                                    placeholder="Choose a quote character"
                                    value={this.state.fileInfo.quotechar}
                                    onChange={this.onQuoteCharChange}
                                />
                                <Form.Select fluid required label="First line is header"
                                    options={[
                                        {'key': 1, text: 'Yes', value: 1},
                                        {'key': 0, text: 'No', value: 0},
                                    ]}
                                    value={this.state.fileInfo.hasHeader}
                                    onChange={this.onHasHeaderChange}
                                />
                            </Form.Group>
                            <Form.Group widths="equal">
                                <Form.Select fluid required label="When inserting data that already exists in system"
                                    options={[
                                        {'key': 0, text: 'Keep the data in the system', value: 'keep_existing'},
                                        {'key': 1, text: 'Replace with new data in CSV', value: 'use_new'},
                                    ]}
                                    value={this.state.resolveConflicts}
                                    onChange={this.onConflictsResolveStrategyChange}
                                />
                            </Form.Group>
                            <Form.Group widths="equal">
                                <Form.Field style={{width: '100%'}}>
                                    <label>Preview</label>
                                    <CsvTable addressBooks={this.state.fileInfo.sampleData}/>
                                </Form.Field>
                            </Form.Group>
                        </Form>
                        }
                    </Modal.Content>
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={this.onClose}>
                        <Icon name="remove" /> Close
                    </Button>
                    {this.state.uploadedFile &&
                    <Button color="green"
                        loading={this.state.confirmLoading}
                        onClick={this.onConfirm}
                        disabled={this.state.hasError}
                    >
                        <Icon name="checkmark" /> Confirm
                    </Button>}
                </Modal.Actions>
            </Modal>
        );
    }

    onEncodingChange = (e: any, data: DropdownProps) => {
        this.setState({
            ...this.state,
            fileInfo: {
                ...this.state.fileInfo,
                encoding: String(data.value),
            }
        },            this.getFileInfo);
    }

    onDelimiterChange = (e: any, data: DropdownProps) => {
        this.setState({
            ...this.state,
            fileInfo: {
                ...this.state.fileInfo,
                delimiter: String(data.value)
            }
        },            this.getFileInfo);
    }

    onHasHeaderChange = (e: any, data: DropdownProps) => {
        this.setState({
            ...this.state,
            fileInfo: {
                ...this.state.fileInfo,
                hasHeader: Boolean(data.value)
            }
        },            this.getFileInfo);
    }

    onQuoteCharChange = (e: any, data: DropdownProps) => {
        this.setState({
            ...this.state,
            fileInfo: {
                ...this.state.fileInfo,
                quotechar: String(data.value)
            }
        },            this.getFileInfo);
    }

    onConflictsResolveStrategyChange = (e: any, data: DropdownProps) => {
        this.setState({
            ...this.state,
            resolveConflicts: String(data.value)
        });
    }
}
