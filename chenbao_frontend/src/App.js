import React, { Component } from 'react';
import './App.css';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Home from "./components/Home";
import PersonHistory from "./components/PersonHistory";
import PersonStat from "./components/PersonStat";
import TotalStat from "./components/TotalStat";
import {MySider} from "./components/MyLayout";

class App extends Component {
  render() {
    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Router>
                <MySider/>
                <Route exact path="/" component={Home} />
                <Route path="/PersonHistory" component={PersonHistory} />
                <Route path="/PersonStat" component={PersonStat} />
                <Route path="/TotalStat" component={TotalStat} />
            </Router>
        </Layout>
    );
  }
}

export default App;
