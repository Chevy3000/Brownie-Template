import React from 'react';
import { DAppProvider, ChainId } from '@usedapp/core';
import { Header } from "./components/Header";
import Container from '@material-ui/core/Container/Container';
function App() {
  return (
    <DAppProvider config={{
      supportedChains: [ChainId.Sepolia]
    }}>
      <Header />
      <Container maxWidth="md">
        <div>Hi!</div>
      </Container>

    </DAppProvider>
  )
}

export default App;
