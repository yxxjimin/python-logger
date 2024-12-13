from logger import Logger


def main():
    logger = Logger.get_logger('root', filename='example.log')

    logger.debug('Initialized database connection pool with 10 connections.')
    logger.info('Server started successfully on port 8080')
    logger.warning('Slow query detected: execution time 3.8 seconds')
    logger.error('Failed to insert record into `orders` table. Integrity constraint violated')
    logger.critical('Out-of-memory error occurred while processing large request')


if __name__ == '__main__':
    main()
