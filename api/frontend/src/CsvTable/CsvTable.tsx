import * as React from 'react';
import { Table, Label, Menu, Icon } from 'semantic-ui-react';
import { getAddressBooks } from './actions';

export type AddressBook = {
    id: number,
    name: String,
    email: String
};

export type CsvTableProps = {
    addressBooks: Array<AddressBook>,
    children?: React.ReactNode,
};

export const CsvTable: React.StatelessComponent<CsvTableProps> = (props: CsvTableProps) => {
    return (
        <Table celled>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Name</Table.HeaderCell>
                    <Table.HeaderCell>Email</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
        
            <Table.Body>
                {props.addressBooks && props.addressBooks.map(
                    (addressBook: AddressBook, index: number) => {
                        return (<Table.Row key={index}>
                            <Table.Cell>{addressBook.name}</Table.Cell>
                            <Table.Cell>{addressBook.email}</Table.Cell>
                        </Table.Row>);
                    }
                )}
            </Table.Body>
        </Table>
    );
};

export type CsvTableState = {
    addressBooks: Array<AddressBook>
};

export class CsvTableComponent extends React.Component<{}, CsvTableState> {

    constructor(props: any) {
        super(props);
        this.state = {
            addressBooks: []
        };
    }

    render() {
        return <CsvTable addressBooks={this.state.addressBooks}/>;
    }

    componentDidMount() {
        getAddressBooks((r: Array<AddressBook>) => {
            this.setState({
                ...this.state,
                addressBooks: r
            });
        });
    }
}