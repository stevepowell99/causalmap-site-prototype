function handler(event) {
  return {
    statusCode: 301,
    statusDescription: 'Moved Permanently',
    headers: { location: { value: 'https://garden.causalmap.app/' } }
  };
}
