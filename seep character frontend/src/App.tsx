import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import LoadingScreen from './components/LoadingScreen';
import ChatInterface from './components/ChatInterface';
import CharacterProfile from './components/CharacterProfile';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={LandingPage} />
        <Route path="/loading" component={LoadingScreen} />
        <Route path="/chat" component={ChatInterface} />
        <Route path="/character/:id" component={CharacterProfile} />
      </Switch>
    </Router>
  );
};

export default App;