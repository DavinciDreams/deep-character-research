// pages/_error.tsx
import React from 'react';
import { NextPageContext } from 'next';

type ErrorProps = {
  statusCode?: number;
  err?: Error;
};

function getStatusMessage(statusCode?: number) {
  if (!statusCode) return 'An unexpected error has occurred.';
  if (statusCode === 404) return 'This page could not be found.';
  return `An error ${statusCode} occurred on server.`;
}

const Error = ({ statusCode }: ErrorProps) => (
  <div style={{
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'sans-serif',
    background: '#fff',
    color: '#333'
  }}>
    <h1>{statusCode || 'Error'}</h1>
    <p>{getStatusMessage(statusCode)}</p>
  </div>
);

Error.getInitialProps = ({ res, err }: NextPageContext) => {
  const statusCode = res?.statusCode ?? err?.statusCode ?? 500;
  return { statusCode };
};

export default Error;