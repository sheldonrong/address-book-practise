import * as React from 'react';
import { CsvTableComponent } from './CsvTable';
import { Upload } from './Upload';
import 'semantic-ui/dist/semantic.css';

import './App.css';

export class App extends React.Component {

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Address Book Manager</h1>
        </header>
        <div>
          <Upload />
        </div>
        <CsvTableComponent />
      </div>
    );
  }
}
