import { useState } from 'react';
import axios from '../Services/api';

const ProfileForm = ({ type }) => {
  const [profile, setProfile] = useState({ name: '', email: '', service: '' });

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post(`/api/${type}-profile`, profile);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="name" placeholder="Name" onChange={handleChange} />
      <input type="email" name="email" placeholder="Email" onChange={handleChange} />
      {type === 'service-provider' && (
        <input type="text" name="service" placeholder="Service Offered" onChange={handleChange} />
      )}
      <button type="submit">Create Profile</button>
    </form>
  );
};
export default ProfileForm;