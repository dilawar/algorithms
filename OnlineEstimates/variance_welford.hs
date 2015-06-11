-- Implementation of Welford method.


import Data.List as L
import System.Random

{-online_single_pass (l1:l2:ls) = compute ls ((l1*l1+l2*l2)/2) 0.0 0 where -}
online_single_pass :: Fractional a => [a] -> a
online_single_pass (l:ls) = compute ls l l 1 where
        compute (x:xs) sos mean n 
            | null xs = a/(n+1) - u*u
            | otherwise = compute xs a u (n+1) 
            where 
                a = sos + x*x
                u = (n*mean + x)/(n+1)

welford :: Fractional a => [a] -> a
welford (x1:x2:xs) = helper xs 0.0 (x1+x2/2) 3 where
    helper [] var _ _ = var
    helper (y:ys) var mean n = helper ys newvar newmean (n+1) where 
        newmean = ((n-1)*mean + y) / n
        newvar = (y - mean)*(y - newmean) / (n-1)

main = do
    seed <- newStdGen
    let d = randoms seed :: [Double]
    let var1 = online_single_pass $ take 1000000 d
    {-let var1 = online_single_pass [1,2,3,4,5]-}
    print $ "Two pass: " ++ show var1
