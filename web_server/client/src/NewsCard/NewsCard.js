import React from 'react'
import './NewsCard.css';
import Auth from '../Auth/Auth';

class NewsCard extends React.Component{
  redirectToUrl(url, e) {
    this.sendClickLog();
    e.preventDefault();
    window.open(url, '_blank');
  }

  sendClickLog() {
    console.log("click on news");
    const url = 'http://' + window.location.hostname + ':3000' 
      + '/news/userId=' + Auth.getEmail() + '&newsId=' + this.props.news.digest;
      console.log(url);
      const request = new Request(
      encodeURI(url),
      {
        method: 'POST',
        headers:{ 'Authorization': 'bearer ' + Auth.getToken() }
      });
    // don't care for the response
    fetch(request);
  }

  render() {
    return(
      <div className = "news-container" onClick = {(e) => this.redirectToUrl(this.props.news.url, e)}>
        <div className='card-panel z-depth-3'>
          <div className="row">
            <div className='col s4 fill'>
              <img src={this.props.news.urlToImage} alt='news'/>
            </div>
            <div className="col s1"/>
            <div className="col s7">
              <div className="news-intro-col">
                <div className="news-intro-panel">
                  <h4>{this.props.news.title}</h4>
                  <div className="news-description">
                    <p>{this.props.news.description}</p>
                    <div>
                      {this.props.news.source != null && <div className='chip light-blue news-chip'>{this.props.news.source}</div>}
                      {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                      {this.props.news.class != null && <div className='chip pink news-chip'>{this.props.news.class}</div>}
                      {this.props.news.time != null && <div className='chip amber news-chip'>{this.props.news.time}</div>}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

}

export default NewsCard;