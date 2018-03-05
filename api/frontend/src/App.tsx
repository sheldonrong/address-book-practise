import * as React from 'react';
import { Container } from 'semantic-ui-react';
import { CsvTableComponent } from './CsvTable';
import { Upload } from './Upload';
import 'semantic-ui/dist/semantic.css';

import './App.css';

type AppState = {
  key: number
};

export class App extends React.Component<{}, AppState> {

  constructor(props: any) {
    super(props);
    this.state = {
        key: 1
    };
  }

  reMount = () => {
    this.setState({
      ...this.state,
      key: this.state.key + 1
    });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Address Book Manager</h1>
        </header>
        <div>
          <Upload onUploadComplete={this.reMount}/>
        </div>
        <Container>
          <CsvTableComponent key={`csv-table-${this.state.key}`} />
        </Container>
      </div>
    );
  }
}
