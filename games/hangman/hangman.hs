-- Game of Hangman.
-- Dilawar, 2013
-- Wed 09 Oct 2013 02:15:02 PM IST, Removed few bugs.
-- Hangman guesses the word from a word list and user does not type it.

import System.IO
import System.Random 
import qualified Data.List as L

getWord :: IO String
getWord = do
    c <- getChar
    if c == '\n'
        then return ""
        else do
            l <- getWord
            return (c:l)

posChar :: [Char] -> Char ->  [Bool]
posChar [] char = []
posChar (x:xs) char = (x==char) : (posChar xs char)


ifContain :: [Char] -> Char -> Bool
ifContain word c = foldr (||) False (posChar word c)


randomWord words = do 
   let ls = lines words 
   let maxLines = length ls
   ns <- randomRIO (0, maxLines)
   return (ls !! ns)
    

addGuessToWord :: [Char] -> [Char] -> Char -> [Char]
addGuessToWord w w1 c 
    | length(w) /= length(w1) = error "Length mismatch" -- just for safety.
    | ifContain w c = buildW1 w1 c (posChar w c)
    | otherwise = w1

buildW1 :: [Char] -> Char -> [Bool] -> [Char]
buildW1 (x:[]) c (p:[])
    | x == '_' && p == True = c:[]
    | x /= '_'  = x:[]
    | otherwise = '_':[]
buildW1 (x:xs) c (p:ps)
    | x == '_' && p == True = c:buildW1 xs c ps
    | x /= '_'  = x:buildW1 xs c ps
    | otherwise = '_' : buildW1 xs c ps


callHangman :: Int -> [Char] -> [Char] -> Char -> IO ()
-- This is the base case 
callHangman n wrd wrd1 ' ' = do 
    putStr ("Guess (Left " ++ (show $ n)++")  : ")
    guess <- getChar
    callHangman (n) wrd wrd1 guess
    
{- No attempt left, you are dead -}
callHangman 1 wrd wrd1 c = do putStrLn "Dead" 
{- Attempts left, play on! -}
callHangman n wrd wrd1 c 
    | ifContain wrd c = do 
        let newWrd = addGuessToWord wrd wrd1 c
        putStrLn ("\t Your progress : " ++ (show newWrd) ++ "\n")
        if wrd == newWrd
            then do
                  putStrLn "Well done!"
            else do
                putStr ("Guess (Left " ++ (show $ n)++")  : ")
                guess <- getChar
                callHangman (n) wrd newWrd guess
    | not (ifContain wrd c) = do
        putStr ("\n"++ "Wrong (Left " ++ (show $ n-1)++")  : ")
        guess <- getChar
        callHangman (n-1) wrd wrd1 guess
    | otherwise = error "Something wrong in logic."

main :: IO ()
main = do
    words <- readFile "./words"
    word <- randomWord words 
    let n = (length word)
    putStrLn $ "+------------------------------------------------------+"
    putStrLn $ "|          GAME OF HANGMAN (IIT Bombay)                |"
    putStrLn $ "+------------------------------------------------------+"
    putStrLn ""
    putStrLn $ "HANGMAN: I have a word of length "++show n++" in my mind!"
    let emptyWrd = foldr(\x->('_':)) [] word --create a masked copy of word.
    putStrLn $ emptyWrd++"\n"
    callHangman (n+1) word emptyWrd ' ' -- dummy call to start the game.
    putStrLn "Game over" -- make sure you are alive ;-)
