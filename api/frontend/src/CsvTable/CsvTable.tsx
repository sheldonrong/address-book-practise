import * as React from 'react';
import { Table, Menu, Icon } from 'semantic-ui-react';
import { getAddressBooks, getTotalPages } from './actions';

export type AddressBook = {
    id: number,
    name: String,
    email: String
};

export type CsvTableProps = {
    preview?: boolean, // is it in preview mode?
    pageSize: number,
    currentPage: number,
    totalPages: number,
    addressBooks: Array<AddressBook>,
    children?: React.ReactNode,
    goToPage: (p: number | string) => any,
};

export const CsvTable: React.StatelessComponent<CsvTableProps> = (props: CsvTableProps) => {
    const range = (start: number, end: number) => {
        return Array.apply(0, Array(end - start))
            .map(function (element: any, index: number) { 
            return index + start;  
        });
    };

    return (
        <Table celled sortable>
            <Table.Header>
                <Table.Row>
                    {!props.preview && <Table.HeaderCell>ID</Table.HeaderCell>}
                    <Table.HeaderCell>Name</Table.HeaderCell>
                    <Table.HeaderCell>Email</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
        
            <Table.Body>
                {props.addressBooks && props.addressBooks.map(
                    (addressBook: AddressBook, index: number) => {
                        return (<Table.Row key={index}>
                            {!props.preview && <Table.Cell>{addressBook.id}</Table.Cell>}
                            <Table.Cell>{addressBook.name}</Table.Cell>
                            <Table.Cell>{addressBook.email}</Table.Cell>
                        </Table.Row>);
                    }
                )}
            </Table.Body>

            {!props.preview &&
            <Table.Footer>
                <Table.Row>
                    <Table.HeaderCell colSpan="3">
                    <Menu floated="right" pagination>
                        <Menu.Item as="a" icon onClick={() => props.goToPage('first')}>
                            <Icon name="angle double left" />
                        </Menu.Item>
                        <Menu.Item as="a" icon onClick={() => props.goToPage('prev')}>
                            <Icon name="angle left" />
                        </Menu.Item>
                        {range(
                            Math.max(0, props.currentPage - 3),
                            Math.min(props.totalPages, props.currentPage + 3),
                        ).map((index: number) => {
                            return (<Menu.Item key={index} as="a" onClick={
                                () => props.goToPage(index)
                            }>{index + 1}</Menu.Item>);
                        })}
                        <Menu.Item as="a" icon onClick={() => props.goToPage('next')}>
                            <Icon name="angle right" />
                        </Menu.Item>
                        <Menu.Item as="a" icon onClick={() => props.goToPage('last')}>
                            <Icon name="angle double right" />
                        </Menu.Item>
                    </Menu>
                    </Table.HeaderCell>
                </Table.Row>
            </Table.Footer>}
        </Table>
    );
};

export type CsvTableState = {
    pageSize: number,
    currentPage: number,
    totalPages: number,
    addressBooks: Array<AddressBook>
};

export class CsvTableComponent extends React.Component<{}, CsvTableState> {

    DEFAULT_PAGE_SIZE = 20;

    constructor(props: any) {
        super(props);
        this.state = {
            pageSize: this.DEFAULT_PAGE_SIZE,
            currentPage: 0,
            totalPages: 1,
            addressBooks: []
        };
    }

    render() {
        return (
            <CsvTable
                addressBooks={this.state.addressBooks}
                currentPage={this.state.currentPage}
                pageSize={this.state.pageSize}
                totalPages={this.state.totalPages}
                goToPage={this.goToPage}
            />
        );
    }

    componentWillMount() {
        getTotalPages(this.state.pageSize, (r: any) => {
            this.setState({
                ...this.state,
                totalPages: r.body.total_pages
            },            this.getAddressBooks);
        });
    }

    getAddressBooks = () => {
        getAddressBooks((r: any) => {
            this.setState({
                ...this.state,
                addressBooks: r.body
            });
        },              this.state.currentPage, this.DEFAULT_PAGE_SIZE);
    }

    goToPage = (p: any) => {
        if (p === 'next') {
            this.setState({
                ...this.state,
                currentPage: Math.min(this.state.currentPage + 1, this.state.totalPages - 1)
            },            this.getAddressBooks);
        } else if (p === 'prev') {
            this.setState({
                ...this.state,
                currentPage: Math.max(0, this.state.currentPage - 1)
            },            this.getAddressBooks);
        } else if (p === 'first') {
            this.setState({
                ...this.state,
                currentPage: 0
            },            this.getAddressBooks);
        } else if (p === 'last') {
            this.setState({
                ...this.state,
                currentPage: this.state.totalPages - 1
            },            this.getAddressBooks);
        } else {
            this.setState({
                ...this.state,
                currentPage: parseInt(p, 10)
            },            this.getAddressBooks);
        }
    }
}