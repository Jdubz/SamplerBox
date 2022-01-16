import React, {useEffect, useState} from 'react';
import axios from 'axios';
import styled from 'styled-components';

const Container = styled.section`
    margin: 0 auto;
    width: 900px;
`

const Devices = () => {
    const [devices, setDevices] = useState([]);

    const getDevices = async () => {
        const {data} = await axios.get('http://sampler/audiodevice');
        setDevices(data);
    }

    useEffect(() => {
        getDevices();
    }, []);

    return <Container>
        <ul>
            {devices.map((device, i) =>
                <li key={device.name}>
                    <h3>{i}. {device.name}</h3>
                    <table>
                    {Object.entries(device).map(([key, value]) => {
                        if (key !== 'name') {
                            return <tr><td>{key}</td><td>{value}</td></tr>
                        }
                    })}
                    </table>
                </li>
            )}
        </ul>
    </Container>;
}

export default Devices;

