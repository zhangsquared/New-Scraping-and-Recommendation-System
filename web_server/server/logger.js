// logging
var winston = require('winston');

var logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  timestamp: true,
  transports: [
    // - Write to all logs with level `info` and below to `activity.log` 
    // - Write all logs error (and below) to `error.log`.
    new (winston.transports.Console)({ 
      colorize: true
    }),
    new winston.transports.File({ 
      filename:  './error.log', 
      level: 'error'
    }),
    new winston.transports.File({ 
      filename:  './activity.log'
    })
  ]
});

module.exports = logger;