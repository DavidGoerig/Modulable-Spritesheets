import React from 'react';
import Home from './components/Home/Home';
import './App.css';
import { isAuthenticated } from './utils/authUtils';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';

const App: React.FC = () => {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/" exact component={Home} />
                </Switch>
            </div>
        </Router>
    );
};

export default App;