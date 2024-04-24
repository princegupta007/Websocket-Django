import React from 'react';
import { render, fireEvent, act, waitFor, MemoryRouter } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from './components/Header';
import PrivateRoute from './utils/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import { getItemFromLocalStorage, setItemToLocalStorage, removeItemFromLocalStorage } from './utils/localStorage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import CreateEntityForm from './pages/CreateEntityForm';
import AuthContext from './context/AuthContext';




describe('Header Component', () => {
  test('renders correctly when user is logged in', () => {
    const { getByText } = render(
      <AuthContext.Provider value={{ userId: 'user123', logoutUser: jest.fn() }}>
        <Router>
          <Header />
        </Router>
      </AuthContext.Provider>
    );
    expect(getByText('Logout')).toBeInTheDocument();
  });

  test('renders correctly when user is not logged in', () => {
    const { getByText } = render(
      <AuthContext.Provider value={{ userId: null, logoutUser: jest.fn() }}>
        <Router>
          <Header />
        </Router>
      </AuthContext.Provider>
    );
    expect(getByText('Login')).toBeInTheDocument();
  });

  test('clicking on logout button calls logoutUser function', () => {
    const logoutUser = jest.fn();
    const { getByText } = render(
      <AuthContext.Provider value={{ userId: 'user123', logoutUser }}>
        <Router>
          <Header />
        </Router>
      </AuthContext.Provider>
    );
    fireEvent.click(getByText('Logout'));
    expect(logoutUser).toHaveBeenCalledTimes(1);
  });
});


// Write test cases for AuthProvider component similarly to Header component tests




describe('AuthProvider Component', () => {
  test('provides correct context values when user is logged in', async () => {
    // Mock localStorage functions
    const mockLocalStorage = {};
    global.localStorage = {
      getItem: jest.fn((key) => mockLocalStorage[key]),
      setItem: jest.fn((key, value) => (mockLocalStorage[key] = value)),
      removeItem: jest.fn((key) => delete mockLocalStorage[key]),
    };

    // Mock fetch function
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => ({
        access: 'access_token',
        refresh: 'refresh_token',
        user_id: 'user123',
        user_type: 'admin',
      }),
    });

    let component;
    await act(async () => {
      component = render(
        <AuthProvider>
          <AuthContext.Consumer>
            {(value) => (
              <div>
                <span>UserId: {value.userId}</span>
                <span>UserType: {value.userType}</span>
              </div>
            )}
          </AuthContext.Consumer>
        </AuthProvider>
      );
    });

    expect(component.getByText('UserId: user123')).toBeInTheDocument();
    expect(component.getByText('UserType: admin')).toBeInTheDocument();
  });

  test('provides correct context values when user is not logged in', async () => {
    // Mock localStorage functions
    const mockLocalStorage = {};
    global.localStorage = {
      getItem: jest.fn((key) => mockLocalStorage[key]),
      setItem: jest.fn((key, value) => (mockLocalStorage[key] = value)),
      removeItem: jest.fn((key) => delete mockLocalStorage[key]),
    };

    // Mock fetch function
    global.fetch = jest.fn().mockResolvedValueOnce({
      ok: false,
      json: () => ({ error: 'Login failed' }),
    });

    let component;
    await act(async () => {
      component = render(
        <AuthProvider>
          <AuthContext.Consumer>
            {(value) => (
              <div>
                <span>UserId: {value.userId}</span>
                <span>UserType: {value.userType}</span>
              </div>
            )}
          </AuthContext.Consumer>
        </AuthProvider>
      );
    });

    expect(component.getByText('UserId:')).toBeInTheDocument();
    expect(component.getByText('UserType:')).toBeInTheDocument();
  });
});


// Write test cases for CreateEntityForm component similarly to Header component tests



describe('CreateEntityForm Component', () => {
  test('renders form correctly', () => {
    const { getByLabelText, getByText } = render(<CreateEntityForm />);
    expect(getByLabelText('Username')).toBeInTheDocument();
    expect(getByLabelText('First Name')).toBeInTheDocument();
    expect(getByLabelText('Last Name')).toBeInTheDocument();
    expect(getByLabelText('Email')).toBeInTheDocument();
    expect(getByLabelText('Mobile')).toBeInTheDocument();
    expect(getByLabelText('Password')).toBeInTheDocument();
    expect(getByText('Create Entity')).toBeInTheDocument();
  });

  test('handles user input correctly', () => {
    const { getByLabelText } = render(<CreateEntityForm />);
    const usernameInput = getByLabelText('Username');
    const firstNameInput = getByLabelText('First Name');
    const lastNameInput = getByLabelText('Last Name');
    const emailInput = getByLabelText('Email');
    const mobileInput = getByLabelText('Mobile');
    const passwordInput = getByLabelText('Password');

    fireEvent.change(usernameInput, { target: { value: 'testUser' } });
    fireEvent.change(firstNameInput, { target: { value: 'John' } });
    fireEvent.change(lastNameInput, { target: { value: 'Doe' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(mobileInput, { target: { value: '1234567890' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(usernameInput.value).toBe('testUser');
    expect(firstNameInput.value).toBe('John');
    expect(lastNameInput.value).toBe('Doe');
    expect(emailInput.value).toBe('test@example.com');
    expect(mobileInput.value).toBe('1234567890');
    expect(passwordInput.value).toBe('password123');
  });

  test('submits form correctly', async () => {
    const mockFetch = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: () => ({ message: 'Entity created successfully' }),
    });
    global.fetch = mockFetch;

    const { getByText, getByLabelText } = render(<CreateEntityForm />);

    fireEvent.change(getByLabelText('Username'), { target: { value: 'testUser' } });
    fireEvent.change(getByLabelText('First Name'), { target: { value: 'John' } });
    fireEvent.change(getByLabelText('Last Name'), { target: { value: 'Doe' } });
    fireEvent.change(getByLabelText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.change(getByLabelText('Mobile'), { target: { value: '1234567890' } });
    fireEvent.change(getByLabelText('Password'), { target: { value: 'password123' } });

    fireEvent.click(getByText('Create Entity'));

    await waitFor(() => expect(mockFetch).toHaveBeenCalledTimes(1));
    expect(mockFetch).toHaveBeenCalledWith('http://192.168.0.224:8000/components/create_admin/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: 'testUser',
        firstname: 'John',
        lastname: 'Doe',
        email: 'test@example.com',
        mobile: '1234567890',
        password: 'password123',
      }),
    });
  });

  test('handles form submission error correctly', async () => {
    const mockFetch = jest.fn().mockResolvedValueOnce({
      ok: false,
      json: () => ({ error: 'Failed to create entity' }),
    });
    global.fetch = mockFetch;

    const { getByText, getByLabelText } = render(<CreateEntityForm />);

    fireEvent.change(getByLabelText('Username'), { target: { value: 'testUser' } });
    fireEvent.change(getByLabelText('First Name'), { target: { value: 'John' } });
    fireEvent.change(getByLabelText('Last Name'), { target: { value: 'Doe' } });
    fireEvent.change(getByLabelText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.change(getByLabelText('Mobile'), { target: { value: '1234567890' } });
    fireEvent.change(getByLabelText('Password'), { target: { value: 'password123' } });

    fireEvent.click(getByText('Create Entity'));

    await waitFor(() => expect(mockFetch).toHaveBeenCalledTimes(1));
    expect(mockFetch).toHaveBeenCalledWith('http://192.168.0.224:8000/components/create_admin/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: 'testUser',
        firstname: 'John',
        lastname: 'Doe',
        email: 'test@example.com',
        mobile: '1234567890',
        password: 'password123',
      }),
    });

    expect(getByText('Failed to create entity')).toBeInTheDocument();
  });
});




// Write test cases for Dashboard component similarly to Header component tests



describe('Dashboard Component', () => {
  test('renders loading state initially', () => {
    const { getByText } = render(<Dashboard />);
    expect(getByText('Loading...')).toBeInTheDocument();
  });

  test('renders admins and users data when fetched successfully', async () => {
    const mockData = {
      admins: [{ id: 1, admin_username: 'admin1', admin_firstname: 'John', admin_lastname: 'Doe', admin_email: 'admin@example.com', admin_mobile: '1234567890' }],
      users: [{ id: 1, user_username: 'user1', user_firstname: 'Jane', user_lastname: 'Smith', user_email: 'user@example.com', user_mobile: '9876543210' }],
      admin_count: 1,
      user_count: 1,
    };

    global.fetch = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
    });

    const { findByText } = render(<Dashboard />);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(global.fetch).toHaveBeenCalledWith('http://192.168.0.224:8000/components/dashboard/', {
        method: 'GET',
        headers: { Authorization: 'Bearer null' }, // Adjust as per your authentication logic
      });
    });

    expect(await findByText('Admins (1):')).toBeInTheDocument();
    expect(await findByText('Users (1):')).toBeInTheDocument();
    expect(await findByText('Username: admin1')).toBeInTheDocument();
    expect(await findByText('Username: user1')).toBeInTheDocument();
  });

  test('renders error message when data fetching fails', async () => {
    global.fetch = jest.fn().mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ error: 'Failed to fetch data' }),
    });

    const { findByText } = render(<Dashboard />);

    expect(await findByText('Error: Failed to fetch data')).toBeInTheDocument();
  });
});

// Write test cases for LoginPage component similarly to Header component tests



describe('LoginPage Component', () => {
  test('renders form correctly', () => {
    const { getByLabelText, getByText } = render(<LoginPage />);
    expect(getByLabelText('Username')).toBeInTheDocument();
    expect(getByLabelText('Password')).toBeInTheDocument();
    expect(getByText('Login')).toBeInTheDocument();
  });

  test('handles user input correctly', () => {
    const { getByLabelText } = render(<LoginPage />);
    const usernameInput = getByLabelText('Username');
    const passwordInput = getByLabelText('Password');

    fireEvent.change(usernameInput, { target: { value: 'testUser' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    expect(usernameInput.value).toBe('testUser');
    expect(passwordInput.value).toBe('password123');
  });

  test('submits form correctly', async () => {
    const mockFetch = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: () => ({ access: 'access_token', refresh: 'refresh_token', user_id: 'user123', user_type: 'admin' }),
    });
    global.fetch = mockFetch;

    const { getByText, getByLabelText } = render(<LoginPage />);

    fireEvent.change(getByLabelText('Username'), { target: { value: 'testUser' } });
    fireEvent.change(getByLabelText('Password'), { target: { value: 'password123' } });

    fireEvent.click(getByText('Login'));

    await waitFor(() => expect(mockFetch).toHaveBeenCalledTimes(1));
    expect(mockFetch).toHaveBeenCalledWith('http://192.168.0.224:8000/account/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'testUser', password: 'password123' }),
    });
  });

  test('handles form submission error correctly', async () => {
    const mockFetch = jest.fn().mockResolvedValueOnce({
      ok: false,
      json: () => ({ error: 'Invalid username or password' }),
    });
    global.fetch = mockFetch;

    const { getByText, getByLabelText } = render(<LoginPage />);

    fireEvent.change(getByLabelText('Username'), { target: { value: 'testUser' } });
    fireEvent.change(getByLabelText('Password'), { target: { value: 'password123' } });

    fireEvent.click(getByText('Login'));

    await waitFor(() => expect(mockFetch).toHaveBeenCalledTimes(1));
    expect(getByText('Invalid username or password')).toBeInTheDocument();
  });
});



// Write test cases for localStorage utility functions (getItemFromLocalStorage, setItemToLocalStorage, removeItemFromLocalStorage)
// Test cases should cover setting, getting, and removing items from local storage



describe('localStorage Utility Functions', () => {
  beforeEach(() => {
    localStorage.clear(); // Clear localStorage before each test
  });

  test('setItemToLocalStorage function sets item correctly', () => {
    setItemToLocalStorage('testKey', 'testValue');
    expect(localStorage.getItem('testKey')).toBe('testValue');
  });

  test('getItemFromLocalStorage function retrieves item correctly', () => {
    localStorage.setItem('testKey', 'testValue');
    const item = getItemFromLocalStorage('testKey');
    expect(item).toBe('testValue');
  });

  test('getItemFromLocalStorage function returns null if item does not exist', () => {
    const item = getItemFromLocalStorage('nonExistentKey');
    expect(item).toBeNull();
  });

  test('removeItemFromLocalStorage function removes item correctly', () => {
    localStorage.setItem('testKey', 'testValue');
    removeItemFromLocalStorage('testKey');
    expect(localStorage.getItem('testKey')).toBeNull();
  });

  test('removeItemFromLocalStorage function does not throw error if item does not exist', () => {
    expect(() => {
      removeItemFromLocalStorage('nonExistentKey');
    }).not.toThrow();
  });
});



// Write test cases for PrivateRoute component to ensure it redirects to login page when user is not logged in
// Test cases should cover both scenarios: user logged in and user not logged in





describe('PrivateRoute Component', () => {
  test('redirects to login page when user is not logged in', () => {
    const TestComponent = () => <div>Private Component</div>;
    const { getByText } = render(
      <MemoryRouter initialEntries={['/private']} initialIndex={0}>
        <AuthProvider>
          <PrivateRoute>
            <TestComponent />
          </PrivateRoute>
        </AuthProvider>
      </MemoryRouter>
    );
    expect(getByText('Login')).toBeInTheDocument();
  });

  test('renders private component when user is logged in', () => {
    const TestComponent = () => <div>Private Component</div>;
    const { getByText } = render(
      <MemoryRouter initialEntries={['/private']} initialIndex={0}>
        <AuthProvider>
          <PrivateRoute>
            <TestComponent />
          </PrivateRoute>
        </AuthProvider>
      </MemoryRouter>
    );
    expect(getByText('Private Component')).toBeInTheDocument();
  });
});
