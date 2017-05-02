import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Container, List, Image, Form, Label, Input } from 'semantic-ui-react';
import { openProfile } from '../actions/victims';
import { tuneFilter } from '../actions/user';
import './search.css';

class Search extends Component {
  onItemClick (data) {
    console.log('onItemClick', data);
  }
  render () {
    const { items, readiness, face, similarity, onChangeReadiness, onChangeFace, onChangeSimilarity } = this.props;
    const { onItemClick } = this;
    return <div className="page__wrap">
      <Container>
        <Form>
          <Label>
            <span className="filter__title">Ready for relationships</span>
            <Input type="range" min="0" max="max" step="1" value={readiness} onChange={onChangeReadiness}/>
          </Label>
          <Label>
            <span className="filter__title">Face</span>
            <Input type="range" min="0" max="max" step="1" value={face} onChange={onChangeFace}/>
          </Label>
          <Label>
            <span className="filter__title">Habit similarity</span>
            <Input type="range" min="0" max="max" step="1" value={similarity} onChange={onChangeSimilarity}/>
          </Label>
        </Form>
      </Container>
      <Container text>
        <List>
          {items.map((item, i) => <List.Item onClick={onItemClick} key={i}>
            <Image avatar src={item.avatar}/>
            <List.Content>
              <List.Header as='a'>{item.name}</List.Header>
              <List.Description>{item.about}</List.Description>
            </List.Content>
          </List.Item>)}
        </List>
      </Container>
    </div>;
  }
}
const ms2p = (state) => ({
  items: state.get('victims').get('items'),
  readiness: state.get('user').get('filters').get('readiness'),
  face: state.get('user').get('filters').get('face'),
  similarity: state.get('user').get('filters').get('similarity'),
});
const md2a = ({
  onChangeReadiness: tuneFilter('readiness'),
  onChangeFace: tuneFilter('face'),
  onChangeSimilarity: tuneFilter('similarity'),
});
export default connect(ms2p, md2a)(Search);
