import { TelegramUser } from '@/global';
import { TCourse } from '@/lib/types';
import React, {
  createContext,
  useState,
  useEffect,
  ReactNode,
  useContext,
} from 'react';

interface UserContextProps {
  user: TelegramUser | null;
  course: TCourse | null;
  setCourse: (course: TCourse | null) => void;
  setUser: React.Dispatch<React.SetStateAction<TelegramUser | null>>;
  isLoading: boolean;
  addTokens: any;
  retractTokens: any;
}

export const UserContext = createContext<UserContextProps | undefined>(undefined);

interface GlobalProviderProps {
  children: ReactNode;
}

export const GlobalProvider: React.FC<GlobalProviderProps> = ({ children }) => {
  const [user, setUser] = useState<TelegramUser | null>(null);
  const [course, setCourseData] = useState<TCourse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  
  const setCourse = (course: TCourse | null) => {
    setCourseData(course);
  }

  function addTokens(quantity: number){
    if (user?.tokens_balance){
      user.tokens_balance+=50*quantity;
    }
  }
  function retractTokens(){
    if (user?.tokens_balance && user.tokens_balance>=500){
      user.tokens_balance-=500;
    }
  }

  useEffect(() => {
    if (window.Telegram?.WebApp) {
      const { WebApp } = window.Telegram;

      WebApp.ready();

      const userData = WebApp.initDataUnsafe.user;
      console.log(userData);
      if (userData) {
        fetch(`https://telegram-mini-app-x496.onrender.com/users/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({user_id: userData.id}),
        })
          .then((response) => response.json())
          .then((data) => {
            setUser({...data, ...userData});
          });
      } else {
        console.warn('User data is undefined.');
        setUser(null);
      }
    } else {
      console.warn('Not running inside Telegram.');
      setUser({
        id: 0,
        first_name: 'Developer',
        last_name: 'User',
        tokens_balance: 0,
        photo_url: ""
      });
    }
    setIsLoading(false);
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser, setCourse, course, isLoading, addTokens, retractTokens }}>
      {children}
    </UserContext.Provider>
  );
};

export const useGlobalContext = (): UserContextProps => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useGlobalContext must be used within a GlobalProvider');
  }
  return context;
};
