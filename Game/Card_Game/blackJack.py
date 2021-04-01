import toy_box
import random

game_flag = True

#Black_Jack
class game:

    basick_stock = []
    stock = []
    bj_game = True
    bj_game_loop_player = True
    bj_game_loop_dealer = True
    bj_game_battle_flag = False

    dealer_hand = []
    player_hand = []

    player_hand_sum = 0
    dealer_hand_sum = 0


    def init_black_jack(self):
        self.basick_stock.clear()
        self.stock.clear()
        self.bj_game = True
        self.bj_game_loop_player = True
        self.bj_game_loop_dealer = True
        self.bj_game_battle_flag = False
        self.dealer_hand.clear()
        self.player_hand.clear()
        self.player_hand_sum = 0
        self.dealer_hand_sum = 0
        

    
    def return_stock(self):

        self.basick_stock = toy_box.stock
        self.basick_stock.pop()
        self.basick_stock.pop()

        for i in self.basick_stock:
            if i[1] > 10:
                i[1] = 10
            elif i[1] == 1:
                i[1] = 11

            self.stock.append(i)

        return self.stock
            



    def game_loop(self,bj_stock):

        while self.bj_game:
            #Game preparation
            random.shuffle(bj_stock)
            self.stock = bj_stock
            self.dealer_hand.append(self.stock[0])
            self.dealer_hand.append(self.stock[1])
            self.stock.pop(0)
            self.stock.pop(0)
            self.player_hand.append(self.stock[0])
            self.player_hand.append(self.stock[1])
            self.stock.pop(0)
            self.stock.pop(0)
            
            print("---------------------<Black_Jack>-------------------------")
 
            print("ディーラーの１枚目のカードは{}です。".format(self.dealer_hand[0][0]))
            print("あなたの手札は{}".format(self.player_hand[0][0]) + "と{}です。".format(self.player_hand[1][0]))
            print("----------------------------------------------------------")

            if self.player_hand[0][1] + self.player_hand[1][1] == 21:
                self.player_hand_sum = 21
                print("Black_Jack!!")
                print("手番をディーラーに渡します。")
                print("----------------------------------------------------------")
                self.bj_game_loop_player = False
            else:
                print("あなたの手番を開始します。")


            #Game start
            #Playerの手番
            while self.bj_game_loop_player:

                self.player_hand_sum = 0
                player_hand_sum_key = 0
                player_hand_sum_key = len(self.player_hand) - 1
                player_hand_A_key = len(self.player_hand) - 1
                
                while player_hand_sum_key >= 0:

                    self.player_hand_sum += self.player_hand[player_hand_sum_key][1]                    
                    player_hand_sum_key -= 1

                    #Aがあるときに合計21をこえたら、Aを1とする。
                    if self.player_hand_sum > 21:
                        while player_hand_A_key >= 0:
                            if self.player_hand[player_hand_A_key][1] == 11:
            
                                self.player_hand[player_hand_A_key][1] = 1
                                self.player_hand_sum = 0
                                player_hand_sum_key = len(self.player_hand) - 1 
                                print("手札が21をこえたため、Aを{}として扱います。".format(self.player_hand[player_hand_A_key][1])) 
                              
                            player_hand_A_key -= 1
                 
                #合計が21を超えたら負け
                if self.player_hand_sum > 21:
                    
                    print("----------------------------------------------------------")
                    print("あなたの手札の合計が21をこえました。")
                    print("あなたの負けです。")
                    self.bj_game_loop_player = False
                    self.bj_game_loop_dealer = False
                    break

                print("あなたの手札の合計は{}です。".format(self.player_hand_sum))
                print("カードを引きますか？")
                print("カードを引く場合は Y 、手番を終了する場合は N を押してください。")

                input_key = input(">> ")
                if input_key in ['y', 'Y']:
                    self.player_hand.append(self.stock[0])
                    print("{}をひきました。".format(self.stock[0][0]))
                    print(self.player_hand)
                    self.stock.pop(0)

                elif input_key in ['n', 'N']:
                    print("合計{}で手番をディーラーへ渡します。".format(self.player_hand_sum))
                    print("----------------------------------------------------------")
                    print("ディーラーの手番を開始します。")
                    self.bj_game_loop_player = False


            #ディーラーの手番
            while self.bj_game_loop_dealer:
                
                dealer_hand_sum_key = 0
                self.dealer_hand_sum = 0
                dealer_hand_sum_key = len(self.dealer_hand) - 1
                dealer_hand_A_key = len(self.player_hand) - 1
                
                while dealer_hand_sum_key >= 0:

                    self.dealer_hand_sum += self.dealer_hand[dealer_hand_sum_key][1]                    
                    dealer_hand_sum_key -= 1

                    #Aがあるときに合計21をこえたら、Aを1とする。
                    if self.dealer_hand_sum > 21:
                        while dealer_hand_A_key >= 0:
                            print("dealer_hand_A_key")
                            print(dealer_hand_A_key)
                            if self.dealer_hand[dealer_hand_A_key][1] == 11:
            
                                self.dealer_hand[dealer_hand_A_key][1] = 1
                                self.dealer_hand_sum = 0
                                dealer_hand_sum_key = len(self.dealer_hand) - 1 
                                print("手札が21をこえたため、Aを{}として扱います。".format(self.dealer_hand[dealer_hand_A_key][1])) 
                            
                            dealer_hand_A_key -= 1

                #合計が２１を超えたら負け
                if self.dealer_hand_sum > 21:
                    print("----------------------------------------------------------")
                    print("ディーラー手札の合計が21をこえました。")
                    print("あなたの勝ちです。")
                    self.bj_game_loop_dealer = False
                    break

                print("ディーラーの手札の合計は{}です。".format(self.dealer_hand_sum))

                if self.dealer_hand_sum < 17:
                    self.dealer_hand.append(self.stock[0])
                    print("ディーラーは{}をひきました。".format(self.stock[0][0]))
                    print(self.dealer_hand)
                    self.stock.pop(0)
                
                elif self.dealer_hand_sum >= 17:
                    print("ディーラーは合計{}で手番を終了します。".format(self.dealer_hand_sum))
                    self.bj_game_loop_dealer = False
                    self.bj_game_battle_flag = True


            if self.bj_game_battle_flag == True:
                print("----------------------------------------------------------")
                print("あなたの手札の合計は{}。".format(self.player_hand_sum))
                print("ディーラーの手札の合計は{}。".format(self.dealer_hand_sum))

                if self.player_hand_sum > self.dealer_hand_sum:
                    print("あなたの勝ちです。")            
                elif self.player_hand_sum < self.dealer_hand_sum:
                    print("ディーラーの勝ちです。")   
                elif self.player_hand_sum == self.dealer_hand_sum:
                    print("引き分けです。")
                

            self.bj_game = False


if __name__=="__main__":
    while game_flag:

        g = game()
        g.init_black_jack
        Stock_BJ = g.return_stock()
        g.game_loop(Stock_BJ)
        print("もう一度プレイしますか？")
        print("続ける場合は Y 、やめる場合は N を押してください。")
        input_key = input(">> ")
        if input_key in ['y', 'Y']:

            print("もう一度プレイします。")    

        elif input_key in ['n', 'N']:
            
            game_flag = False
    
