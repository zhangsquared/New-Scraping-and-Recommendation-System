import React from 'react';
import registerServiceWorker from './registerServiceWorker';
import Base from './Base/Base';
import ReactDOM from 'react-dom';

ReactDOM.render(<Base />, document.getElementById('root'));
// client can get files from cache when internet is slow
registerServiceWorker();
