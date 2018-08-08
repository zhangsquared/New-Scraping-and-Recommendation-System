import './NewsPanel.css';

import Auth from '../Auth/Auth';
import NewsCard from '../NewsCard/NewsCard';
import React from 'react';
import _ from 'lodash';

class NewsPanel extends React.Component {
  constructor(){
    super();
    this.state = { 
      news: null, // list of NewsCard
      pageNum: 1, 
      loadedAll: false
    }; 
  }

  componentDidMount(){
    this.loadMoreNews();
    // call loadMoreNews() once per second
    this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
    window.addEventListener('scroll', () => this.handleScroll());
  }

  handleScroll(){
    let scrollY = window.scrollY 
      || window.pageYOffset 
      || document.documentElement.scrollTop;
    let delta = document.body.offsetHeight - (window.innerHeight + scrollY);
    if(delta <= 50) {
      this.loadMoreNews();
    }
  }

  loadMoreNews() {
    console.log("load more news");

    if(this.state.loadedAll === true){
      return;
    }

    // const news_url = 'http://' + window.location.hostname + ':3000/news/userId=' 
    //   + encodeURIComponent(Auth.getEmail()) + "&pageNum=" + this.state.pageNum;

      const news_url = 'http://' + window.location.hostname + ':3000/news/userId=' 
      + Auth.getEmail() + "&pageNum=" + this.state.pageNum;
    
    // escape special char in email, so encodeURI
    const request = new Request(encodeURI(news_url), {
      method: 'GET',
      headers: {
        'Authorization': 'bearer '+ Auth.getToken(),
      }
    });

    fetch(request)
      .then(res => res.json())
      .then(j => {
        if(!j || j.length == 0){
          this.setState({ loadedAll: true })
        }
        this.setState({
          news: this.state.news ? this.state.news.concat(j) : j,
          pageNum: this.state.pageNum + 1
      });
    });
  }

  renderNews() {
    // if a list contains components, it requires "key attribute to identify each component"
    // then virtual DOM can quicky idendify the components in the list.
    const news_list = this.state.news.map(news => {
      return(
        <a className = 'list-group-item' href='#'>
          <NewsCard news = {news}/>
        </a>
      );
    });

    return(
      <div className ='contianer-fluid'>
        <div className = "list-group">
          {news_list}
        </div>
      </div>
    )
  }

  render() {
    if(this.state.news){
      return(
        <div>
          {this.renderNews()}
        </div>
      )
    } else {
      return(
        <div id = 'msg-app-loading'>
          Loading...
        </div>
      )
    }
  }
}

export default NewsPanel;