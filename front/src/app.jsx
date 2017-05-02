import React, { Component } from 'react';
import { Route, NavLink } from 'react-router-dom';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { getPageData } from './actions/pages';

class NavLinkM extends Component {
  render = () => <NavLink activeClassName="_current" {...this.props}/>;
}

import { getPageName } from './utils';
import './app.css';

import Index from './pages/index'
import Search from './pages/search';
import Profile from './pages/profile';
import Events from './pages/events';

const CustomRoute = ({ component: Component, hook, ...rest }) => (
  <Route {...rest} render={props => {
    hook(props.match);
    return <Component {...props}/>
  }}/>
)

// export default
class App extends Component {
  render() {
    const { onPageOpen } = this.props;
    return <div className={`app page_${getPageName.call(this)}`}>
      <header className="app-header">
        <NavLinkM to="/"><span className="logo">❤️ Dating App</span></NavLinkM>
      </header>
      <main>
        <CustomRoute hook={onPageOpen} exact path="/" component={Index}/>
        <CustomRoute hook={onPageOpen} path="/search" component={Search}/>
        <CustomRoute hook={onPageOpen} path="/profile" component={Profile}/>
        <CustomRoute hook={onPageOpen} path="/events" component={Events}/>
      </main>
      <footer></footer>
    </div>;
  }
}


App.contextTypes = {
  router: PropTypes.object.isRequired,
};

const mapDispatchToProps = ({onPageOpen: getPageData});

export default connect(null, mapDispatchToProps)(App);
